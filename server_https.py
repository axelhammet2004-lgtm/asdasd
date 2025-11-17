#!/usr/bin/env python3
"""
Servidor HTTPS local para ESP Web Flasher
Genera un certificado autofirmado temporal
"""

import http.server
import ssl
import os
import sys
from pathlib import Path

PORT = 8443  # Puerto HTTPS estándar alternativo

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler con CORS habilitado para Web Serial API"""
    
    def end_headers(self):
        # Habilitar CORS para Web Serial API
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Headers para Web Serial API
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def generate_selfsigned_cert():
    """Genera un certificado SSL autofirmado"""
    try:
        from OpenSSL import crypto
        
        # Crear par de llaves
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        
        # Crear certificado
        cert = crypto.X509()
        cert.get_subject().C = "CL"
        cert.get_subject().O = "Wilobu"
        cert.get_subject().CN = "localhost"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)  # 1 año
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')
        
        # Guardar archivos
        with open("cert.pem", "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        with open("key.pem", "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        
        return True
    except ImportError:
        return False

def main():
    print("")
    print("="*70)
    print("   SERVIDOR HTTPS PARA FLASHER WILOBU v2.1")
    print("="*70)
    print("")
    
    # Verificar si existen los certificados
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        print("Generando certificado SSL autofirmado...")
        if not generate_selfsigned_cert():
            print("⚠️  No se pudo generar el certificado automáticamente.")
            print("   Instalando pyOpenSSL...")
            os.system(f"{sys.executable} -m pip install pyOpenSSL --quiet")
            if not generate_selfsigned_cert():
                print("❌ Error: No se pudo generar el certificado.")
                print("   El servidor se iniciará sin HTTPS (puede fallar Web Serial).")
                input("Presiona Enter para continuar de todos modos...")
        else:
            print("✓ Certificado generado")
    
    print("")
    print("Iniciando servidor HTTPS en puerto", PORT)
    print("")
    print("="*70)
    print("   INSTRUCCIONES:")
    print("="*70)
    print("")
    print("1. Abre Google Chrome")
    print(f"2. Navega a: https://localhost:{PORT}")
    print("")
    print("3. ⚠️  Chrome mostrará: 'Tu conexión no es privada'")
    print("   Esto es NORMAL (es un certificado autofirmado)")
    print("")
    print("4. Haz clic en: 'Avanzado' → 'Acceder a localhost (no seguro)'")
    print("")
    print("5. Conecta tu ESP32 al USB")
    print("6. Haz clic en 'INSTALAR FIRMWARE'")
    print("")
    print("="*70)
    print("")
    print("Servidor corriendo... (Presiona Ctrl+C para detener)")
    print("")
    
    try:
        # Crear servidor HTTP
        server = http.server.HTTPServer(('', PORT), CORSHTTPRequestHandler)
        
        # Envolver con SSL si existen los certificados
        if os.path.exists("cert.pem") and os.path.exists("key.pem"):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain('cert.pem', 'key.pem')
            server.socket = context.wrap_socket(server.socket, server_side=True)
            print(f"✓ Servidor HTTPS corriendo en: https://localhost:{PORT}")
        else:
            print(f"⚠️  Servidor HTTP corriendo en: http://localhost:{PORT}")
            print("   (Web Serial API puede fallar sin HTTPS)")
        
        print("")
        
        # Abrir navegador
        import webbrowser
        webbrowser.open(f"https://localhost:{PORT}")
        
        # Iniciar servidor
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n")
        print("Servidor detenido.")
        print("")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
