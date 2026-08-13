<<<<<<< HEAD
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- -----------------------------------------------------
-- Schema voiture_estoque
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema voiture_estoque
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS voiture_estoque DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE voiture_estoque ;

-- -----------------------------------------------------
-- Table cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente (
  id INT NOT NULL AUTO_INCREMENT,
  cliente_nome VARCHAR(45) NOT NULL,
  cliente_cnpj VARCHAR(14) NOT NULL,
  cliente_cep VARCHAR(8) NOT NULL,
  cliente_email VARCHAR(50) NOT NULL,
  cliente_ddi VARCHAR(2) NOT NULL,
  cliente_ddd VARCHAR(2) NOT NULL,
  cliente_telefone VARCHAR(20) NOT NULL,
  cliente_descricao VARCHAR(700) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table funcionario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS funcionario (
  id INT NOT NULL AUTO_INCREMENT,
  funcionario_nome VARCHAR(50) NOT NULL,
  funcionario_senha VARCHAR(200) NOT NULL,
  funcionario_cpf VARCHAR(11) NOT NULL,
  funcionario_cep VARCHAR(8) NOT NULL,
  funcionario_email VARCHAR(100) NOT NULL,
  funcionario_ddi VARCHAR(2) NOT NULL,
  funcionario_ddd VARCHAR(2) NOT NULL,
  funcionario_telefone VARCHAR(20) NOT NULL,
  funcionario_cargo VARCHAR(50) NOT NULL,
  funcionario_permissao VARCHAR(50) NOT NULL,
  imagem_nome VARCHAR(255) NULL,
  imagem_tipo VARCHAR(100) NULL,
  imagem_blob LONGBLOB NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


SHOW WARNINGS;

-- -----------------------------------------------------
-- Table fornecedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS fornecedor (
  id INT NOT NULL AUTO_INCREMENT,
  fornecedor_nome VARCHAR(45) NOT NULL,
  fornecedor_cnpj VARCHAR(14) NOT NULL,
  fornecedor_cep VARCHAR(8) NOT NULL,
  fornecedor_email VARCHAR(50) NOT NULL,
  fornecedor_ddi VARCHAR(2) NOT NULL,
  fornecedor_ddd VARCHAR(2) NOT NULL,
  fornecedor_telefone VARCHAR(20) NOT NULL,
  fornecedor_descricao VARCHAR(700) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table produto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS produto (
  id INT NOT NULL AUTO_INCREMENT,
  produto_nome VARCHAR(50) NOT NULL,
  produto_descricao VARCHAR(600) NOT NULL,
  produto_categoria VARCHAR(50) NOT NULL,
  produto_quantidade_minima INT NOT NULL,
  produto_preco_custo DECIMAL(10,2) NOT NULL,
  produto_preco_venda DECIMAL(10,2) NOT NULL,
  produto_peso DECIMAL(10,3) NOT NULL,
  produto_localizacao VARCHAR(50) NOT NULL,
  imagem_nome VARCHAR(255) NULL,
  imagem_tipo VARCHAR(100) NULL,
  imagem_blob LONGBLOB NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table empilhadeira
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS empilhadeira (
  id INT NOT NULL AUTO_INCREMENT,
  empilhadeira_chassi VARCHAR(20) NOT NULL,
  empilhadeira_status VARCHAR(10) NOT NULL,
  empilhadeira_modelo VARCHAR(30) NOT NULL,
  empilhadeira_marca VARCHAR(30) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table estoque
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS estoque (
  id INT NOT NULL AUTO_INCREMENT,
  estoque_quantidade INT NOT NULL,
  produto_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_estoque_produto_idx (produto_id ASC) VISIBLE,
  CONSTRAINT fk_estoque_produto
    FOREIGN KEY (produto_id)
    REFERENCES produto (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SHOW WARNINGS;



-- -----------------------------------------------------
-- Table uso_empilhadeira
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS uso_empilhadeira (
  id INT NOT NULL AUTO_INCREMENT,
  uso_empilhadeira_datahora DATETIME NOT NULL,
  funcionario_id INT NOT NULL,
  empilhadeira_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_uso_empilhadeira_funcionario1_idx (funcionario_id ASC) VISIBLE,
  INDEX fk_uso_empilhadeira_empilhadeira1_idx (empilhadeira_id ASC) VISIBLE,
  CONSTRAINT fk_uso_empilhadeira_funcionario1
    FOREIGN KEY (funcionario_id)
    REFERENCES funcionario (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_uso_empilhadeira_empilhadeira1
    FOREIGN KEY (empilhadeira_id)
    REFERENCES empilhadeira (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table pedido_entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido_entrada (
  id INT NOT NULL AUTO_INCREMENT,
  status_pedido_entrada VARCHAR(30) NOT NULL,
  fornecedor_id INT NOT NULL,
  data_pedido_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX fk_pedido_entrada_fornecedor1_idx (fornecedor_id ASC) VISIBLE,
  CONSTRAINT fk_pedido_entrada_fornecedor1
    FOREIGN KEY (fornecedor_id)
    REFERENCES fornecedor (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SHOW WARNINGS;

-- -----------------------------------------------------
-- Table pedido_saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido_saida (
  id INT NOT NULL AUTO_INCREMENT,
  status_pedido_saida VARCHAR(30) NOT NULL,
  cliente_id INT NOT NULL,
  data_pedido_saida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX fk_pedido_saida_cliente1_idx (cliente_id ASC) VISIBLE,
  CONSTRAINT fk_pedido_saida_cliente1
    FOREIGN KEY (cliente_id)
    REFERENCES cliente (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table detalhe_entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS detalhe_entrada (
  id INT NOT NULL AUTO_INCREMENT,
  detalhe_entrada_quantidade INT NOT NULL,
  produto_id INT NOT NULL,
  pedido_entrada_id INT NOT NULL,
  detalhe_entrada_item INT NOT NULL,
  PRIMARY KEY (id, pedido_entrada_id),
  INDEX fk_detalhe_entrada_estoque1_idx (produto_id ASC) VISIBLE,
  INDEX fk_detalhe_entrada_pedido_entrada1_idx (pedido_entrada_id ASC) VISIBLE,
  CONSTRAINT fk_detalhe_entrada_estoque1
    FOREIGN KEY (produto_id)
    REFERENCES estoque (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_detalhe_entrada_pedido_entrada1
    FOREIGN KEY (pedido_entrada_id)
    REFERENCES pedido_entrada (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SHOW WARNINGS;

-- -----------------------------------------------------
-- Table movimentacao_entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS movimentacao_entrada (
  id INT NOT NULL AUTO_INCREMENT,
  datahora_movimentacao_entrada DATETIME NOT NULL,
  detalhe_entrada_id INT NOT NULL,
  detalhe_entrada_pedido_entrada_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_movimentacao_entrada_detalhe_entrada1_idx (detalhe_entrada_id ASC, detalhe_entrada_pedido_entrada_id ASC) VISIBLE,
  CONSTRAINT fk_movimentacao_entrada_detalhe_entrada1
    FOREIGN KEY (detalhe_entrada_id , detalhe_entrada_pedido_entrada_id)
    REFERENCES detalhe_entrada (id , pedido_entrada_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table detalhe_saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS detalhe_saida (
  id INT NOT NULL AUTO_INCREMENT,
  detalhe_saida_quantidade INT NOT NULL,
  pedido_saida_id INT NOT NULL,
  produto_id INT NOT NULL,
  detalhe_saida_item INT NOT NULL,
  PRIMARY KEY (id, pedido_saida_id),
  INDEX fk_detalhe_saida_pedido_saida1_idx (pedido_saida_id ASC) VISIBLE,
  INDEX fk_detalhe_saida_estoque1_idx (produto_id ASC) VISIBLE,
  CONSTRAINT fk_detalhe_saida_pedido_saida1
    FOREIGN KEY (pedido_saida_id)
    REFERENCES pedido_saida (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_detalhe_saida_estoque1
    FOREIGN KEY (produto_id)
    REFERENCES estoque (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table movimentacao_saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS movimentacao_saida (
  id INT NOT NULL AUTO_INCREMENT,
  datahora_movimentacao_saida DATETIME NOT NULL,
  detalhe_saida_id INT NOT NULL,
  detalhe_saida_pedido_saida_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_movimentacao_saida_detalhe_saida1_idx (detalhe_saida_id ASC, detalhe_saida_pedido_saida_id ASC) VISIBLE,
  CONSTRAINT fk_movimentacao_saida_detalhe_saida1
    FOREIGN KEY (detalhe_saida_id , detalhe_saida_pedido_saida_id)
    REFERENCES detalhe_saida (id , pedido_saida_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

=======
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


select * from funcionario;
-- -----------------------------------------------------
-- Schema voiture_estoque
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema voiture_estoque
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS voiture_estoque DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE voiture_estoque ;

-- -----------------------------------------------------
-- Table cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente (
  id INT NOT NULL AUTO_INCREMENT,
  cliente_nome VARCHAR(45) NOT NULL,
  cliente_cnpj VARCHAR(14) NOT NULL,
  cliente_cep VARCHAR(8) NOT NULL,
  cliente_email VARCHAR(50) NOT NULL,
  cliente_ddi VARCHAR(2) NOT NULL,
  cliente_ddd VARCHAR(2) NOT NULL,
  cliente_telefone VARCHAR(20) NOT NULL,
  cliente_descricao VARCHAR(700) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table funcionario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS funcionario (
  id INT NOT NULL AUTO_INCREMENT,
  funcionario_nome VARCHAR(50) NOT NULL,
  funcionario_senha VARCHAR(200) NOT NULL,
  funcionario_cpf VARCHAR(11) NOT NULL,
  funcionario_cep VARCHAR(8) NOT NULL,
  funcionario_email VARCHAR(100) NOT NULL,
  funcionario_ddi VARCHAR(2) NOT NULL,
  funcionario_ddd VARCHAR(2) NOT NULL,
  funcionario_telefone VARCHAR(20) NOT NULL,
  funcionario_cargo VARCHAR(50) NOT NULL,
  funcionario_permissao VARCHAR(50) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


SHOW WARNINGS;

-- -----------------------------------------------------
-- Table fornecedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS fornecedor (
  id INT NOT NULL AUTO_INCREMENT,
  fornecedor_nome VARCHAR(45) NOT NULL,
  fornecedor_cnpj VARCHAR(14) NOT NULL,
  fornecedor_cep VARCHAR(8) NOT NULL,
  fornecedor_email VARCHAR(50) NOT NULL,
  fornecedor_ddi VARCHAR(2) NOT NULL,
  fornecedor_ddd VARCHAR(2) NOT NULL,
  fornecedor_telefone VARCHAR(20) NOT NULL,
  fornecedor_descricao VARCHAR(700) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table produto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS produto (
  id INT NOT NULL AUTO_INCREMENT,
  produto_nome VARCHAR(50) NOT NULL,
  produto_descricao VARCHAR(600) NOT NULL,
  produto_categoria VARCHAR(50) NOT NULL,
  produto_quantidade_minima INT NOT NULL,
  produto_preco_custo DECIMAL(10,2) NOT NULL,
  produto_preco_venda DECIMAL(10,2) NOT NULL,
  produto_peso DECIMAL(10,3) NOT NULL,
  produto_localizacao VARCHAR(50) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table empilhadeira
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS empilhadeira (
  id INT NOT NULL AUTO_INCREMENT,
  empilhadeira_chassi VARCHAR(20) NOT NULL,
  empilhadeira_status VARCHAR(10) NOT NULL,
  empilhadeira_modelo VARCHAR(30) NOT NULL,
  empilhadeira_marca VARCHAR(30) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table estoque
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS estoque (
  id INT NOT NULL AUTO_INCREMENT,
  estoque_quantidade INT NOT NULL,
  produto_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_estoque_produto_idx (produto_id ASC) VISIBLE,
  CONSTRAINT fk_estoque_produto
    FOREIGN KEY (produto_id)
    REFERENCES produto (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SHOW WARNINGS;



-- -----------------------------------------------------
-- Table uso_empilhadeira
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS uso_empilhadeira (
  id INT NOT NULL AUTO_INCREMENT,
  uso_empilhadeira_datahora DATETIME NOT NULL,
  funcionario_id INT NOT NULL,
  empilhadeira_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_uso_empilhadeira_funcionario1_idx (funcionario_id ASC) VISIBLE,
  INDEX fk_uso_empilhadeira_empilhadeira1_idx (empilhadeira_id ASC) VISIBLE,
  CONSTRAINT fk_uso_empilhadeira_funcionario1
    FOREIGN KEY (funcionario_id)
    REFERENCES funcionario (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_uso_empilhadeira_empilhadeira1
    FOREIGN KEY (empilhadeira_id)
    REFERENCES empilhadeira (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table pedido_entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido_entrada (
  id INT NOT NULL AUTO_INCREMENT,
  status_pedido_entrada VARCHAR(30) NOT NULL,
  fornecedor_id INT NOT NULL,
  data_pedido_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX fk_pedido_entrada_fornecedor1_idx (fornecedor_id ASC) VISIBLE,
  CONSTRAINT fk_pedido_entrada_fornecedor1
    FOREIGN KEY (fornecedor_id)
    REFERENCES fornecedor (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SHOW WARNINGS;

-- -----------------------------------------------------
-- Table pedido_saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido_saida (
  id INT NOT NULL AUTO_INCREMENT,
  status_pedido_saida VARCHAR(30) NOT NULL,
  cliente_id INT NOT NULL,
  data_pedido_saida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX fk_pedido_saida_cliente1_idx (cliente_id ASC) VISIBLE,
  CONSTRAINT fk_pedido_saida_cliente1
    FOREIGN KEY (cliente_id)
    REFERENCES cliente (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table detalhe_entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS detalhe_entrada (
  id INT NOT NULL AUTO_INCREMENT,
  detalhe_entrada_quantidade INT NOT NULL,
  produto_id INT NOT NULL,
  pedido_entrada_id INT NOT NULL,
  detalhe_entrada_item INT NOT NULL,
  PRIMARY KEY (id, pedido_entrada_id),
  INDEX fk_detalhe_entrada_estoque1_idx (produto_id ASC) VISIBLE,
  INDEX fk_detalhe_entrada_pedido_entrada1_idx (pedido_entrada_id ASC) VISIBLE,
  CONSTRAINT fk_detalhe_entrada_estoque1
    FOREIGN KEY (produto_id)
    REFERENCES estoque (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_detalhe_entrada_pedido_entrada1
    FOREIGN KEY (pedido_entrada_id)
    REFERENCES pedido_entrada (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SHOW WARNINGS;

-- -----------------------------------------------------
-- Table movimentacao_entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS movimentacao_entrada (
  id INT NOT NULL AUTO_INCREMENT,
  datahora_movimentacao_entrada DATETIME NOT NULL,
  detalhe_entrada_id INT NOT NULL,
  detalhe_entrada_pedido_entrada_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_movimentacao_entrada_detalhe_entrada1_idx (detalhe_entrada_id ASC, detalhe_entrada_pedido_entrada_id ASC) VISIBLE,
  CONSTRAINT fk_movimentacao_entrada_detalhe_entrada1
    FOREIGN KEY (detalhe_entrada_id , detalhe_entrada_pedido_entrada_id)
    REFERENCES detalhe_entrada (id , pedido_entrada_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table detalhe_saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS detalhe_saida (
  id INT NOT NULL AUTO_INCREMENT,
  detalhe_saida_quantidade INT NOT NULL,
  pedido_saida_id INT NOT NULL,
  produto_id INT NOT NULL,
  detalhe_saida_item INT NOT NULL,
  PRIMARY KEY (id, pedido_saida_id),
  INDEX fk_detalhe_saida_pedido_saida1_idx (pedido_saida_id ASC) VISIBLE,
  INDEX fk_detalhe_saida_estoque1_idx (produto_id ASC) VISIBLE,
  CONSTRAINT fk_detalhe_saida_pedido_saida1
    FOREIGN KEY (pedido_saida_id)
    REFERENCES pedido_saida (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_detalhe_saida_estoque1
    FOREIGN KEY (produto_id)
    REFERENCES estoque (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table movimentacao_saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS movimentacao_saida (
  id INT NOT NULL AUTO_INCREMENT,
  datahora_movimentacao_saida DATETIME NOT NULL,
  detalhe_saida_id INT NOT NULL,
  detalhe_saida_pedido_saida_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_movimentacao_saida_detalhe_saida1_idx (detalhe_saida_id ASC, detalhe_saida_pedido_saida_id ASC) VISIBLE,
  CONSTRAINT fk_movimentacao_saida_detalhe_saida1
    FOREIGN KEY (detalhe_saida_id , detalhe_saida_pedido_saida_id)
    REFERENCES detalhe_saida (id , pedido_saida_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

>>>>>>> cdac1e4055aa1146cf641e3c23fa71f87bb69f0f
