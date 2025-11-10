import collections

class MemorySimulator:
    def __init__(self, page_size, num_tlb_entries, num_frames, rep_policy, va_bits):
        self.page_size = page_size
        self.num_tlb_entries = num_tlb_entries
        self.num_frames = num_frames    
        self.rep_policy = rep_policy
        self.va_bits = va_bits

        if rep_policy not in ['LRU', 'SecondChance']:
            raise ValueError("Política de substituição inválida. Use 'LRU' ou 'SecondChance'.")

        self.tlb = collections.OrderedDict() 
        self.page_table = collections.OrderedDict()  
        self.frames = [None] * num_frames

        self.valid_bits = {}                          # Bit de validade (por página)
        self.reference_bits = [0] * num_frames        # Para Second Chance
        self.pointer = 0                              # Ponteiro circular (Second Chance)




        # for page in range(va_bits*page_size):
        #     self.page_table[page] = {"valid": False, "frame": -1}





        # contadores de estatísticas
        self.tlb_hits = 0
        self.tlb_misses = 0
        self.page_faults = 0


    def access_memory(self, virtual_address):
        """
        Simula o acesso a um endereço virtual.
        Deve atualizar os contadores e aplicar a política de substituição se necessário.
        """
        page_number = virtual_address // self.page_size

        if page_number in self.tlb:
            self.tlb_hits += 1
            self.tlb.move_to_end(page_number)
            self.page_table.move_to_end(page_number)
            return

        self.tlb_misses += 1
        if page_number not in self.page_table:
            self.page_faults += 1
            frame_number = self._allocate_frame(page_number)
            self.valid_bits[page_number] = True
        else:
            frame_number = self.page_table[page_number]
            if not self.valid_bits.get(page_number, False):
                self.page_faults += 1
                frame_number = self._allocate_frame(page_number)
                self.valid_bits[page_number] = True
                self.page_table.move_to_end(page_number)

        self._update_tlb(page_number, frame_number)

    def _update_tlb(self, page_number, frame_number):
        """Insere ou atualiza a TLB usando política LRU."""
        if page_number in self.tlb:
            self.tlb.move_to_end(page_number)
        else:
            if len(self.tlb) >= self.num_tlb_entries:
                self.tlb.popitem(last=False)
            self.tlb[page_number] = frame_number

    def _allocate_frame(self, page_number):
        """Seleciona um frame para alocar uma página (com substituição se necessário)."""
        if None in self.frames:
            frame_number = self.frames.index(None)
            self.frames[frame_number] = page_number
            self.page_table[page_number] = frame_number
            return frame_number

        if self.rep_policy == "LRU":
            victim_page = next(iter(self.page_table))
            victim_frame = self.page_table[victim_page]
            del self.page_table[victim_page]
        else:
            victim_page, victim_frame = self._select_victim_second_chance()

        self.page_table[page_number] = victim_frame
        self.valid_bits[page_number] = True
        self.valid_bits[victim_page] = False
        return victim_frame

    def _select_victim_second_chance(self):
        """Escolhe vítima usando o algoritmo Second Chance."""
        while True:
            page = self.frames[self.pointer]
            if self.reference_bits[self.pointer] == 0:
                victim_frame = self.pointer
                self.pointer = (self.pointer + 1) % self.num_frames
                return page, victim_frame
            else:
                self.reference_bits[self.pointer] = 0
                self.pointer = (self.pointer + 1) % self.num_frames

    def print_statistics(self):
        print("=" * 60)
        print("SIMULADOR DE MEMÓRIA - Estatísticas de Acesso")
        print("=" * 60)
        print(f"Política de Substituição:   {self.rep_policy}")
        print(f"Tamanho da Página:          {self.page_size} bytes")
        print(f"Entradas na TLB:            {self.num_tlb_entries}")
        print(f"Número de Frames:           {self.num_frames}")
        print("-" * 60)
        print(f"TLB Hits:                   {self.tlb_hits:,}")
        print(f"TLB Misses:                 {self.tlb_misses:,}")
        print(f"Page Faults:                {self.page_faults:,}")
        print("=" * 60)
