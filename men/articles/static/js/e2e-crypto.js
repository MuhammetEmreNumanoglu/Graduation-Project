
'use strict';

// ─── Constants ────────────────────────────────────────────────────────────────

const E2E_PRIVATE_KEY_LS = 'e2e_private_key';
const E2E_PUBLIC_KEY_LS = 'e2e_public_key';

const RSA_PARAMS = {
    name: 'RSA-OAEP',
    modulusLength: 2048,
    publicExponent: new Uint8Array([1, 0, 1]),
    hash: 'SHA-256',
};

const AES_PARAMS = {
    name: 'AES-GCM',
    length: 256,
};

// ─── Utility helpers ──────────────────────────────────────────────────────────

/**
 * Encode an ArrayBuffer as a URL-safe base64 string.
 * @param {ArrayBuffer} buf
 * @returns {string}
 */
function bufToBase64(buf) {
    const bytes = new Uint8Array(buf);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

/**
 * Decode a base64 string back to a Uint8Array.
 * @param {string} b64
 * @returns {Uint8Array}
 */
function base64ToBuf(b64) {
    const binary = atob(b64);
    const buf = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        buf[i] = binary.charCodeAt(i);
    }
    return buf;
}

/**
 * Encode a string as UTF-8 bytes.
 * @param {string} str
 * @returns {Uint8Array}
 */
function encodeText(str) {
    return new TextEncoder().encode(str);
}

/**
 * Decode UTF-8 bytes to a string.
 * @param {Uint8Array} buf
 * @returns {string}
 */
function decodeText(buf) {
    return new TextDecoder().decode(buf);
}

// ─── Key Generation ───────────────────────────────────────────────────────────

/**
 * Generate a new RSA-OAEP key pair and persist it in localStorage.
 * @returns {Promise<CryptoKeyPair>}
 */
async function generateKeyPair() {
    const keyPair = await crypto.subtle.generateKey(
        RSA_PARAMS,
        true, // extractable so we can export/persist
        ['encrypt', 'decrypt']
    );

    // Export and persist both keys
    const publicJwk = await crypto.subtle.exportKey('jwk', keyPair.publicKey);
    const privateJwk = await crypto.subtle.exportKey('jwk', keyPair.privateKey);

    localStorage.setItem(E2E_PUBLIC_KEY_LS, JSON.stringify(publicJwk));
    localStorage.setItem(E2E_PRIVATE_KEY_LS, JSON.stringify(privateJwk));

    return keyPair;
}

/**
 * Load the key pair from localStorage, generating a new one if absent.
 * @returns {Promise<CryptoKeyPair>}
 */
async function getOrCreateKeyPair() {
    const publicJwkStr = localStorage.getItem(E2E_PUBLIC_KEY_LS);
    const privateJwkStr = localStorage.getItem(E2E_PRIVATE_KEY_LS);

    if (publicJwkStr && privateJwkStr) {
        try {
            const publicJwk = JSON.parse(publicJwkStr);
            const privateJwk = JSON.parse(privateJwkStr);

            const publicKey = await crypto.subtle.importKey(
                'jwk', publicJwk,
                { name: 'RSA-OAEP', hash: 'SHA-256' },
                true, ['encrypt']
            );
            const privateKey = await crypto.subtle.importKey(
                'jwk', privateJwk,
                { name: 'RSA-OAEP', hash: 'SHA-256' },
                true, ['decrypt']
            );
            return { publicKey, privateKey };
        } catch (_e) {
            // Keys corrupt or outdated — regenerate
            console.warn('[E2E] Could not load keys from storage, regenerating…');
        }
    }
    return generateKeyPair();
}

/**
 * Upload the local user's public key to the server.
 * Call this once after login / on key generation.
 * @returns {Promise<boolean>} true on success
 */
async function uploadPublicKey() {
    try {
        const publicJwkStr = localStorage.getItem(E2E_PUBLIC_KEY_LS);
        if (!publicJwkStr) return false;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
            || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
            || '';

        const fd = new FormData();
        fd.append('public_key', publicJwkStr);

        const resp = await fetch('/api/e2e/save-public-key/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: fd,
            credentials: 'same-origin',
        });
        const data = await resp.json();
        return data.success === true;
    } catch (err) {
        console.error('[E2E] uploadPublicKey failed:', err);
        return false;
    }
}

/**
 * Fetch the RSA public key (JWK) for a given user from the server.
 * @param {number|string} userId
 * @returns {Promise<CryptoKey|null>}
 */
async function fetchRecipientPublicKey(userId) {
    try {
        const resp = await fetch(`/api/e2e/get-public-key/?user_id=${userId}`, {
            credentials: 'same-origin',
        });
        const data = await resp.json();
        if (!data.success || !data.public_key) return null;
        const jwk = JSON.parse(data.public_key);
        return await crypto.subtle.importKey(
            'jwk', jwk,
            { name: 'RSA-OAEP', hash: 'SHA-256' },
            false, ['encrypt']
        );
    } catch (err) {
        console.error('[E2E] fetchRecipientPublicKey failed:', err);
        return null;
    }
}

// ─── Encrypt ──────────────────────────────────────────────────────────────────

/**
 * Encrypt a plaintext message for a given recipient public key.
 *
 * Returns an object with:
 *   - ciphertext: base64 string  (AES-GCM encrypted message, includes 12-byte IV prefix)
 *   - encryptedKey: base64 string (RSA-OAEP wrapped AES key)
 *
 * @param {CryptoKey} recipientPublicKey  — RSA-OAEP public key of the recipient
 * @param {string}    plaintext
 * @returns {Promise<{ciphertext: string, encryptedKey: string}>}
 */
async function encryptMessage(recipientPublicKey, plaintext) {
    // 1. Generate a fresh random AES-256-GCM key for this message
    const aesKey = await crypto.subtle.generateKey(AES_PARAMS, true, ['encrypt', 'decrypt']);

    // 2. Generate a random 12-byte IV
    const iv = crypto.getRandomValues(new Uint8Array(12));

    // 3. Encrypt the plaintext with AES-GCM
    const ciphertextBuf = await crypto.subtle.encrypt(
        { name: 'AES-GCM', iv },
        aesKey,
        encodeText(plaintext)
    );

    // 4. Prepend IV to ciphertext: [12 bytes IV][rest...]
    const combined = new Uint8Array(iv.byteLength + ciphertextBuf.byteLength);
    combined.set(iv, 0);
    combined.set(new Uint8Array(ciphertextBuf), iv.byteLength);

    // 5. Export raw AES key and wrap it with recipient's RSA-OAEP public key
    const rawAesKey = await crypto.subtle.exportKey('raw', aesKey);
    const wrappedKey = await crypto.subtle.encrypt(
        { name: 'RSA-OAEP' },
        recipientPublicKey,
        rawAesKey
    );

    return {
        ciphertext: bufToBase64(combined),
        encryptedKey: bufToBase64(wrappedKey),
    };
}

// ─── Decrypt ──────────────────────────────────────────────────────────────────

/**
 * Decrypt a message that was encrypted with encryptMessage().
 *
 * @param {string} ciphertextB64   — base64 AES-GCM ciphertext (IV prepended)
 * @param {string} encryptedKeyB64 — base64 RSA-OAEP wrapped AES key
 * @returns {Promise<string>} plaintext, or throws if decryption fails
 */
async function decryptMessage(ciphertextB64, encryptedKeyB64) {
    // Load own private key
    const privateJwkStr = localStorage.getItem(E2E_PRIVATE_KEY_LS);
    if (!privateJwkStr) throw new Error('[E2E] No private key in storage.');

    const privateJwk = JSON.parse(privateJwkStr);
    const privateKey = await crypto.subtle.importKey(
        'jwk', privateJwk,
        { name: 'RSA-OAEP', hash: 'SHA-256' },
        false, ['decrypt']
    );

    // 1. Unwrap AES key
    const wrappedKeyBuf = base64ToBuf(encryptedKeyB64);
    const rawAesKey = await crypto.subtle.decrypt(
        { name: 'RSA-OAEP' },
        privateKey,
        wrappedKeyBuf
    );
    const aesKey = await crypto.subtle.importKey(
        'raw', rawAesKey,
        AES_PARAMS,
        false, ['decrypt']
    );

    // 2. Split combined blob into IV + ciphertext
    const combined = base64ToBuf(ciphertextB64);
    const iv = combined.slice(0, 12);
    const ciphertext = combined.slice(12);

    // 3. Decrypt
    const plaintextBuf = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv },
        aesKey,
        ciphertext
    );

    return decodeText(plaintextBuf);
}

// ─── Initialisation ───────────────────────────────────────────────────────────

/**
 * Initialise E2E encryption for the current user:
 *   1. Load or generate a key pair.
 *   2. Upload the public key to the server (idempotent).
 * Call this once per page load (after DOMContentLoaded).
 * @returns {Promise<void>}
 */
async function initE2E() {
    try {
        await getOrCreateKeyPair();
        await uploadPublicKey();
        console.log('[E2E] Encryption initialised.');
    } catch (err) {
        console.error('[E2E] Initialisation failed:', err);
    }
}

// ─── Exports ──────────────────────────────────────────────────────────────────

window.E2E = {
    initE2E,
    getOrCreateKeyPair,
    generateKeyPair,
    uploadPublicKey,
    fetchRecipientPublicKey,
    encryptMessage,
    decryptMessage,
};
