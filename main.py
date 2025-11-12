from mem_sim import MemorySimulator

def run_simulator(arq_test):
    mem_simulator = MemorySimulator(page_size=4096, 
                                num_tlb_entries=16, 
                                num_frames=64, 
                                rep_policy='LRU')
    for addr in arq_test:
        mem_simulator.access_memory(int(addr))
    mem_simulator.print_statistics()
    print()

test_files = [
    "tests/trace.in",
    "tests/trace_random.in",
    "tests/trace_sequential.in"
]

for arq in test_files:
   run_simulator(open(arq, "r"))
