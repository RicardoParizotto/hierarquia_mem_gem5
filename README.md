# Trabalho_org_gem5

Projeto educacional para estudar organizações de processadores (arquitetura e pipeline) utilizando o simulador **gem5** com suporte a arquitetura RISC-V.

## Objetivo

Este repositório contém exemplos de programas em C compilados para RISC-V e um modelo de processador para simulação em gem5, permitindo analisar como diferentes arquiteturas executam e otimizam o código.

## Pré-requisitos

Certifique-se de ter instalado:
- **GCC para RISC-V**: Compilador que gera código de máquina para arquitetura RISC-V
- **gem5**: Simulador de arquitetura de processadores

## Passo a Passo

### 1. Compilar código C para RISC-V

Compile um programa em C gerando um binário estático RISC-V:

```bash
riscv64-linux-gnu-gcc -static qs.c vetor.c -o qs.riscv
```

**Parâmetros:**
- `-static`: Faz linking estático (importante para simulação em gem5)
- `qs.c`: Arquivo fonte em C
- `-o qs.riscv`: Nome do binário de saída

### 2. Visualizar o Assembly do binário

Para entender como o código foi compilado, você pode desassemblar o binário e ver as instruções RISC-V:

```bash
riscv64-linux-gnu-objdump -d qs.riscv
```

**Parâmetros:**
- `-d`: Desassembla o binário mostrando as instruções em linguagem de assembly

Você também pode redirecionar a saída para um arquivo para análise:

```bash
riscv64-linux-gnu-objdump -d qs.riscv > qs_assembly.txt
```

### 3. Simular a execução em gem5

Execute a simulação do programa usando um dos modelos de processador:

```bash
./gem5/build/RISCV/gem5.opt <model_name>.py --binary programs/<program_name>.riscv
```

**Exemplo:**
```bash
./gem5/build/RISCV/gem5.opt model.py --binary programs/qs.riscv
```
