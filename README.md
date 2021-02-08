# API Python

Aqui detalho alguns detalhes que não estão no código.

## Pipeline CI/CD

Um ponto que não está contemplado no código são os testes e a pipeline de deploy. Vejo isso como algo importante, porém devido ao tempo eu não pude fazer a tempo.
Como ferramenta, eu sempre recomendo utilizar a que está embarcada com a ferramenta de repositório. No caso do github, seria o github actions. 
Como estratégia de branch, o git flow funciona bem na maioria dos projetos de microsserviços que tenham um fluxo de manutenção e evolução alto. Para projetos pequenos como libs, pode-se utilizar uma estratégia menos burocrática como a one-flow;

A pipeline de CI deve ser rodada ao abrir um Pull Request, sendo uma das checagens principais para aprovação, e deve ter os seguintes passos:
- Checkout da aplicação
- Checagem estática de código (lint, sonarqube, etc..)
- Testes unitarios
- Testes de integração


A pipeline de CD deve ser executada ao concluir o PR, realizando o deploy para o ambiente relacionado a branch que recebeu o merge. Ela deve ter, além dos passos do CI, os seguintes passos:
- Build da imagem docker
- Login no repositorio de imagens
- Deploy da imagem para o repositorio
- Atualização do script kubernetes e aplicação no ambiente


## Infraestrutura

![Alt text](diagrama_infra.png?raw=true "Diagrama de infraestrutura")

Para a infraestrutura o planejado é rodar com kubernetes provisionando com terraform.
O Kubernetes traz uma certa independencia de cloud provider, porém o Terraform torna a configuração da estrutura totalmente dependente de uma nuvem, mas é aceitavel, devido a facilidade que o terraform traz para o provisionamento e o gerenciamento da configuração via código, permitindo versionamento e automação.

A configuração dos containeres estão todas via variáveis de ambiente, deixando a aplicação independente de qualquer código fixo. Isso também facilita a manutenção pois não precisamos buildar a aplicação novamente para alterar as configurações, e permite a utilização de cofres de senha como o Vault ou o SSM da AWS.

### Segurança e monitoramento

Para garantir uma centralização e também para deixar o código mais simples, removi do código a responsabilidade de monitoramento e segurança, e deixei para a infraestrutura.

Sendo assim, o API-Gateway fica responsável por verificar o token JWT dos endpoints privados, juntamento com a permissão de acesso. O código fica apenas com algumas verificações de permissões pontuais, conforme a necessidade.

A parte de monitoramento fica por conta do Istio. Utiliza-lo traz, além das necessidades de monitoramento, uma facilidade na implementação pois não precisamos nos preocupar com a criação de correlation-id e o rastreamento das informações em chamadas entre os microsserviços. O unico lugar que ainda precisa configura o correlation é o kafka. Existem ferramentas pagas que fazem isso de forma transparente, porém para o rastramento pode-se utilizar uma lib interna para fazer isso.

## O que faltou?

- Adicionar permissão de acesso.
- Adicionar correlation-id nas mensagens do Kafka.

