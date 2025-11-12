import collections

class MemorySimulator:
    def __init__(self, page_size, num_tlb_entries, num_frames, rep_policy):
        self.page_size = page_size
        self.num_tlb_entries = num_tlb_entries
        self.num_frames = num_frames    
        self.rep_policy = rep_policy

        if rep_policy not in ['LRU', 'SecondChance']:
            raise ValueError("Política de substituição inválida. Use 'LRU' ou 'SecondChance'.")

        self.tlb = collections.OrderedDict() 
        self.page_table = collections.OrderedDict()
        self.frames = [None] * num_frames

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
            if page_number in self.page_table:
                self.page_table.move_to_end(page_number)
            return

        self.tlb_misses += 1

        if page_number not in self.page_table:
            self.page_faults += 1
            frame_number = self._allocate_frame(page_number)
        else:
            frame_number = self.page_table[page_number]
            self.page_table.move_to_end(page_number)

        self._update_tlb(page_number, frame_number)


    def _update_tlb(self, page_number, frame_number):
        """Atualiza ou insere uma página na TLB aplicando a política LRU."""
        if page_number in self.tlb:
            self.tlb.move_to_end(page_number)
        else:
            if len(self.tlb) >= self.num_tlb_entries:
                self.tlb.popitem(last=False)
            self.tlb[page_number] = frame_number

    
    def _allocate_frame(self, page_number):
        """Aloca um frame livre ou substitui a página menos usada (LRU)."""
        
        if None in self.frames:
            frame_number = self.frames.index(None)
            self.frames[frame_number] = page_number
            self.page_table[page_number] = frame_number
            return frame_number

        victim_page = next(iter(self.page_table))
        victim_frame = self.page_table[victim_page]
        self.page_table.pop(victim_page)
        self.frames[victim_frame] = page_number
        self.page_table[page_number] = victim_frame

        return victim_frame


    def print_statistics(self):
        print("=" * 60)
        print("SIMULADOR DE MEMÓRIA - Estatísticas de Acesso")
        print("=" * 60)
        print(f"Política de Substituição:   {self.rep_policy} (TLB e Memória)")
        print(f"Tamanho da Página:          {self.page_size} bytes")
        print(f"Entradas na TLB:            {self.num_tlb_entries}")
        print(f"Número de Frames:           {self.num_frames}")
        print("-" * 60)
        print(f"TLB Hits:                   {self.tlb_hits:,}")
        print(f"TLB Misses:                 {self.tlb_misses:,}")
        print(f"Page Faults:                {self.page_faults:,}")
        print("=" * 60)