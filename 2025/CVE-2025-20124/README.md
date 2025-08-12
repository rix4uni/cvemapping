# CVE-2025-20124 – Cisco ISE 3.0 Java Deserialization Remote Code Execution (RCE)

## 📌 Descrição
Este exploit demonstra a exploração da vulnerabilidade **CVE-2025-20124** no **Cisco Identity Services Engine (ISE)**, onde um endpoint interno de desserialização Java aceita objetos maliciosos enviados pelo cliente, permitindo **execução remota de comandos (RCE)**.

A falha está na ausência de validação durante a desserialização de objetos Java, permitindo que um invasor autenticado envie um *payload* que, ao ser processado, executa comandos arbitrários no sistema.

---

## 🚨 Impacto
- Execução remota de comandos no servidor Cisco ISE
- Possível tomada de controle total do appliance
- Escalonamento para comprometimento da rede corporativa

---

## 🔍 Detalhes Técnicos
- **Produto afetado**: Cisco ISE 3.0
- **Vulnerabilidade**: Java Deserialization sem validação
- **CVE**: CVE-2025-20124
- **Autenticação**: Necessária (session token válido)
- **Vetor de ataque**: HTTP POST para `/api/v1/admin/deserializer` com objeto Java serializado em Base64
- **Exploração**: Uso de *gadget chains* para execução de comandos

---

## 📦 Requisitos
- Python 3.x
- Bibliotecas:
  ```bash
  pip install requests>=2.25.0 urllib3>=1.26.0

## Usage

python3 CVE-2025-20124.py --url https://ise.target.com --session TOKEN --cmd "id"

## Contact
------------
Caso queira me contatar ou precise de algum serviço, me encontre nas seguintes plataformas:

Discord User: 4wj.

Instargram: @glowwz9

Email: vliyanie1337@proton.me
