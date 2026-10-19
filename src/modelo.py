# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the RISCV equivalent to `simple.py` (which is designed to run using the
X86 ISA). More detailed documentation can be found in `simple.py`.
"""

import m5
from m5.objects import *

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource


import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--binary",
    type=str,
    required=True,
    help="Caminho para binario RISC-V"
)
args = parser.parse_args()
binary_path = os.path.abspath(args.binary)

REPLACEMENT_POLICIES = {
    "LRU":      LRURP,
    "Random":   RandomRP,
    "TreePLRU": TreePLRURP,
    "FIFO":     FIFORP,
    "MRU":      MRURP,
}

# 1. Escolhemos o modelo O3 (Out-of-Order) para RISC-V
processor = SimpleProcessor(cpu_type=CPUTypes.O3, num_cores=1, isa=ISA.RISCV)

# 2. Configurao de Memoria e Cache (Obrigatrio para O3)
# Associatividade: 1=mapeamento direto, 2, 4, 8...)
cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="256kB",
    l1d_assoc=2,
    l1i_assoc=2,
    l2_assoc=2,
)


# Política aplicada após criação, pois a stdlib não aceita no construtor
repl = REPLACEMENT_POLICIES[args.repl_policy]()
for l1d in cache_hierarchy.l1dcaches:
    l1d.replacement_policy = "LRU"
for l1i in cache_hierarchy.l1icaches:
    l1i.replacement_policy = "LRU"
cache_hierarchy.l2cache.replacement_policy = "LRU"

memory = SingleChannelDDR4_2400("8GB")

# 3. Montagem da placa
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

binary = BinaryResource(local_path=binary_path)
board.set_se_binary_workload(binary)

# 6. Rodar a simulacao
simulator = Simulator(board=board)
print("Iniciando simulacao O3 RISC-V...")
simulator.run()

print(f"Simulacaoo finalizada no tick {simulator.get_current_tick()}")
