"""
Log Encryption Module

AES-256 encryption for secure log storage.
"""

import os
import base64
import logging
from typing import Optional

logger = logging.getLogger("Keylogger.encrypt")


class LogEncryptor:
    """
    AES-256 encryption for log files.
    
    Uses the cryptography library for secure encryption.
    """
    
    def __init__(self, key: Optional[str] = None):
        """
        Initialize encryptor.
        
        Args:
            key: Optional encryption key (base64 encoded)
        """
        self.key = key
        self._cipher = None
        
        # Try to import cryptography
        try:
            from cryptography.fernet import Fernet
            
            if key:
                # Validate key
                try:
                    base64.b64decode(key)
                    self._key = key.encode()
                except Exception:
                    logger.warning("Invalid key provided, generating new one")
                    self._key = Fernet.generate_key()
            else:
                self._key = Fernet.generate_key()
            
            self._cipher = Fernet(self._key)
            logger.info("Encryptor initialized")
            
        except ImportError:
            logger.error("cryptography not installed. Install with: pip install cryptography")
            raise
    
    def get_key(self) -> str:
        """Get the encryption key (store this securely!)."""
        return self._key.decode()
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Base64 encoded encrypted text
        """
        if not self._cipher:
            return plaintext
        
        try:
            encrypted = self._cipher.encrypt(plaintext.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return plaintext
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext.
        
        Args:
            ciphertext: Base64 encoded encrypted text
            
        Returns:
            Decrypted plaintext
        """
        if not self._cipher:
            return ciphertext
        
        try:
            decoded = base64.b64decode(ciphertext.encode())
            decrypted = self._cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return ciphertext
    
    def decrypt_file(self, input_path: str, output_path: str):
        """
        Decrypt an entire log file.
        
        Args:
            input_path: Path to encrypted log file
            output_path: Path to write decrypted output
        """
        try:
            with open(input_path, 'r') as f:
                lines = f.readlines()
            
            decrypted_lines = []
            for line in lines:
                decrypted = self.decrypt(line.strip())
                decrypted_lines.append(decrypted)
            
            with open(output_path, 'w') as f:
                f.write('\n'.join(decrypted_lines))
            
            logger.info(f"Decrypted log saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"File decryption failed: {e}")
            raise


def generate_key() -> str:
    """Generate a new encryption key."""
    try:
        from cryptography.fernet import Fernet
        return Fernet.generate_key().decode()
    except ImportError:
        logger.error("cryptography not installed")
        raise
