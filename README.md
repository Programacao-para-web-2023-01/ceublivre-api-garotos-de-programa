## Catálogo de produtos

Este microsserviço gerencia a lista de produtos disponíveis no marketplace.

URL da API de produtos
https://ceublivreapi-1-m0315087.deta.app/

### Criação de produtos (2 pontos)

Capacidade de permitir que os vendedores do marketplace criem novos produtos, adicionando informações como nome,
descrição, imagens, preço, categoria, entre outros.
 - POST("*/product"): Cria registro de produto com os atributos nome, descrição, categoria, preço, imagem(nome da imagem) e peso.

### Atualização de produtos (2 pontos)

Capacidade de permitir que os vendedores do marketplace atualizem as informações de produtos existentes, como imagens,
preço, descrição, categoria, entre outros.
 - PUT("*/product/{key}"): Atualiza registro do produto por meio de JSON na query
 - PATCH("*/product/image/{prod_key}"): Insere o nome da imagem no registro do produto e envia arquivo ao banco de armazenamento
 - PATCH("*/product/enable/{key}"): Habilita produto no banco de dados
 - PATCH("*/product/disable/{key}"): Desabilita produto no banco de dados
 - PATCH("*/product/category/{key}"): Insere categoria no registro do produto
 - PATCH("*/product/category/remove/{key}"): Remove categoria do registro de produto

### Exclusão de produtos (1 ponto)

Capacidade de permitir que os vendedores do marketplace excluam produtos que não estejam mais disponíveis ou que não
estejam mais em estoque.
 - DELETE("*/product/{key}"): Deleta registro do produto do banco de dados

### Gerenciamento de categorias de produtos (2 pontos)

Capacidade de permitir que os administradores do marketplace cadastrem, atualizem e excluam possíveis categorias de
produtos.
 - POST("*/category"): Cria registro de categoria
 - GET("*/category"): Lista categorias em registro
 - GET("*/category/{key}"): Lista dados da categoria buscada
 - PUT("*/category/{key}"): Atualiza dados da categoria com a chave correspondente
 - DELETE("*/category/{key}"): Deleta registro da categoria, removendo-a dos registros de produto

### Listar todos os produtos (1 ponto)

Capacidade de listar todos os produtos cadastrados no marketplace.
- GET("*/product"): Lista o JSON de todos os produtos do banco de dados
- GET("*/product/{key}"): Lista o produto com a chave correspondente
- GET("*/product/active"): Lista o JSON de todos os produtos ativos do banco de dados
- GET("*/product/image/{prod_key}"): Retorna imagem do produto com a chave correspondente

### Gerenciamento de variações (1 ponto para cada variação)

Permitir que os vendedores possam criar e gerenciar variações de produtos, como tamanhos, cores, modelos, etc.

### Controle de versão de produtos (3 pontos)

Permitir que os vendedores possam gerenciar diferentes versões de um mesmo produto, como por exemplo, uma nova versão
com um preço atualizado ou uma descrição mais detalhada.

**Total: Pelo menos 11 pontos**
