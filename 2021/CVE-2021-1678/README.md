#  Gerenciamento da implantação de alterações de associação de Impressora RPC para CVE-2021-1678 (KB4599464)

Erro no compartilhamento de impressora do Windows baixe e execute: https://github.com/alvaciroliveira/RpcAuthnLevelPrivacyEnabled/blob/main/RpcAuthnLevelPrivacyEnabled.reg

CRÉDITOS PARA: https://support.microsoft.com/pt-br/topic/gerenciamento-da-implanta%C3%A7%C3%A3o-de-altera%C3%A7%C3%B5es-de-associa%C3%A7%C3%A3o-de-impressora-rpc-para-cve-2021-1678-kb4599464-12a69652-30b9-3d61-d9f7-7201623a8b25

#  *Tome medidas para proteger seu ambiente e evitar interrupções, você deve fazer o seguinte:*

Atualize todos os dispositivos de cliente e servidor instalando a atualização do Windows de 12 de janeiro de 2021 ou uma atualização posterior do Windows. Esteja ciente de que instalar a atualização do Windows não atenua totalmente a vulnerabilidade de segurança e pode impactar sua configuração atual de impressão. Você deve realizar a Etapa 2.

Habilite o modo de Imposição no servidor de impressão.  O modo de Imposição será habilitado em todos os dispositivos Windows no futuro.

#  Importante Você deve reiniciar seu dispositivo depois de instalar essas atualizações necessárias.

Instale a atualização

Para resolver a vulnerabilidade de segurança, instale as atualizações do Windows e habilite o modo de Aplicação seguindo estas etapas:

Implante a atualização de 12 de janeiro de 2021 para todos os dispositivos de cliente e de servidor.

Depois que todos os dispositivos de cliente e servidor foram atualizados, a proteção total pode ser ativada definindo o valor do registro como 1.


#  Etapa 1: Instalar o Windows Update

Instale a atualização do Windows de 12 de janeiro de 2021 ou uma atualização posterior do Windows para todos os dispositivos de cliente e de servidor.
Atualizações de 12 de janeiro de 2021

#  Etapa 2: Habilitar o modo de imposição

Importante Esta seção, método ou tarefa contém etapas que descrevem como modificar o Registro. Entretanto, sérios problemas poderão ocorrer caso você modifique o Registro incorretamente. Portanto, siga essas etapas cuidadosamente. Para obter mais proteção, faça backup do Registro antes de modificá-lo. Dessa forma, você poderá restaurar o Registro se ocorrer um problema. Para saber mais sobre como fazer o backup e restaurar o Registro, consulte Como fazer o backup e restaurar o Registro no Windows.

Depois que todos os dispositivos de cliente e servidor tiverem sido atualizados, você pode ativar a proteção total implantando o modo de Imposição. Para fazer isso, siga estas etapas:
Clique com o botão direito em Iniciar, clique em Executar, digite cmd na caixa Executar e pressione Ctrl+Shift+Enter.
No prompt de comando do Administrador, digite regedit e pressione Enter.
Localize a seguinte subchave do Registro:

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print

Clique com o botão direito em Imprimir, selecione Novo e depois clique em Valor DWORD (32 bits).

Digite:
```bash
RpcAuthnLevelPrivacyEnabled
```
e pressione Enter.

Clique com o botão direito do mouse em RpcAuthnLevelPrivacyEnabled e clique em Modificar.

Na caixa Dados do valor, digite 1 e clique em Ok.

*Observação: Esta atualização introduz suporte para o valor de Registro RpcAuthnLevelPrivacyEnabled para aumentar o nível de autorização para o IRemoteWinspool da impressora.*

Subchave do Registro

HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Print

Valor

RpcAuthnLevelPrivacyEnabled

Tipo de dados

REG_DWORD

#  Dados

+  1: habilita o Modo de Imposição. Antes de ativar o modo de Imposição do lado do servidor, certifique-se de que todos os dispositivos clientes instalaram a atualização do Windows lançada em 12 de janeiro de 2021 ou uma atualização posterior do Windows. Essa correção aumenta o nível de autorização para a interface RPC IRemoteWinspool da impressora e adiciona uma nova política e valor de registro no lado do servidor para obrigar o cliente a usar o novo nível de autorização se o modo de Imposição for aplicado. Se o dispositivo cliente não tiver a atualização de segurança de 12 de janeiro de 2021 ou uma atualização posterior do Windows aplicada, a experiência de impressão será quebrada quando o cliente se conectar ao servidor através da interface IRemoteWinspool.

+ 0: não recomendado. Desativa o nível de autenticação de aumento para o IRemoteWinspool da impressora e seus dispositivos não estão protegidos.

![image](https://github.com/alvaciroliveira/RpcAuthnLevelPrivacyEnabled/assets/129803614/a5ea26e0-24ec-402e-9102-692e328a51e0)

![image](https://github.com/alvaciroliveira/RpcAuthnLevelPrivacyEnabled/assets/129803614/e2f02604-c813-4934-823f-f746eb163f69)


É necessário reiniciar? Sim, uma reinicialização do dispositivo ou uma reinicialização do serviço de spooler é necessária.

Desde já agradeço, estou a disposição mailto:alvacir.oliveira@msn.com
