import uuid
from math import log
from pprint import pprint

class MasterKeySystemGen:
    def __init__(self, _ggmk, _rotation, _kBA, _number_of_pins, _kBA_length, _number_masters, _MACS):
        self.id = uuid.uuid4()
        self.ggmk = _ggmk
        self.rotation = _rotation
        self.kBA = _kBA
        self.number_of_pins = _number_of_pins
        self.kBA_length = _kBA_length
        self.number_masters = _number_masters
        self.MACS = _MACS
        self.max_rotation = len(_rotation)
        self.number_changes = (_kBA_length**self.max_rotation)//_number_masters
        self.page_master_rotations = int(log(_number_masters,_kBA_length))
        self.mks = uuid.uuid4()

    def build_bittings(self, list_bitting):
        topPinBitting = []
        botPinBitting = []
        state = 'Available'
        # use indexer to build bitting
        for o in range(len(self.ggmk)):
            topPin = []
            botPin = []
            if(list_bitting[o] < self.ggmk[o]):
                botPin = int(list_bitting[o])
                topPin = int(self.ggmk[o]) - botPin
            else:
                botPin = int(self.ggmk[o])
                topPin = int(list_bitting[o]) - botPin
    
            topPinBitting.append(str(topPin))
            botPinBitting.append(str(botPin))
            if(o > 0):
                if(abs(int(list_bitting[o])-int(list_bitting[o-1])) > int(self.MACS)):
                    state = 'Discarded'

        xBitting = ''.join(str(e) for e in list_bitting)
        xTopPin = ''.join(str(e) for e in topPinBitting)
        xBotPin = ''.join(str(e) for e in botPinBitting)
        return xBitting, xTopPin, xBotPin, state

    def generate_chk(self, j):
        chk = []
        for i in range(self.max_rotation): ## Required Input = J
            current_column = self.rotation.index(i+1)
            x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
            cut = self.kBA[x][i]
            chk.append(cut)
        return chk

    def generate_block_master(self, j):
        bm = []
        for i in range(self.max_rotation):
            current_column = self.rotation.index(i+1) # returns 5, 4, 3, 2, 1, 0 in stock example
            cut = None
            if current_column == 0:
                cut = self.ggmk[i]
            else:
                x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
                cut = self.kBA[x][i]
            bm.append(cut)
        #print("**Row Master Here: ", bm)
        return bm

    def generate_row_master(self, j):
        rm = []
        for i in range(self.max_rotation):
            current_column = self.rotation.index(i+1) # returns 5, 4, 3, 2, 1, 0 in stock example
            cut = None
            if current_column < 2:
                cut = self.ggmk[i]
            else:
                x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
                cut = self.kBA[x][i]
            rm.append(cut)
        #print("**Row Master Here: ", rm)
        return rm

    def generate_page_master(self, j):
        pm = []
        for i in range(self.max_rotation):
            current_column = self.rotation.index(i+1) # returns 5, 4, 3, 2, 1, 0 in stock example
            cut = None
            if current_column < (self.max_rotation-self.page_master_rotations):
                cut = self.ggmk[i]
            else:
                x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
                cut = self.kBA[x][i]
            pm.append(cut)
        #print("****Page Master Here: ", pm)
        return pm

    def generate_page_block_master(self, j):
        pbm = []
        for i in range(self.max_rotation):
            current_column = self.rotation.index(i+1) # returns 5, 4, 3, 2, 1, 0 in stock example
            cut = None
            if current_column < (self.max_rotation-(self.page_master_rotations-1)):
                cut = self.ggmk[i]
            else:
                x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
                cut = self.kBA[x][i]
            pbm.append(cut)
        #print("******Page Block Master Here: ", pbm)
        return pbm
    
    def generate_page_group_master(self, j):
        pgm = []
        for i in range(self.max_rotation):
            current_column = self.rotation.index(i+1) # returns 5, 4, 3, 2, 1, 0 in stock example
            cut = None
            if current_column < (self.max_rotation-(self.page_master_rotations-2)):
                cut = self.ggmk[i]
            else:
                x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
                cut = self.kBA[x][i]
            pgm.append(cut)
        #print("********Page Group Master Here: ", pgm)
        return pgm

    def generate_page_section_master(self, j):
        psm = []
        for i in range(self.max_rotation):
            current_column = self.rotation.index(i+1) # returns 5, 4, 3, 2, 1, 0 in stock example
            cut = None
            if current_column < (self.max_rotation-(self.page_master_rotations-3)):
                cut = self.ggmk[i]
            else:
                x = (j%(self.kBA_length**(current_column+1))) // (self.kBA_length**current_column)
                cut = self.kBA[x][i]
            psm.append(cut)
        #print("********Page Section Master Here: ", psm)
        return psm

    def build_iterator(self):
        output_system = []
        print(self.rotation)
        pageSectionMaster = None
        pageGroupMaster = None
        pageBlockMaster = None
        pageMaster = None
        rowMaster = None
        blockMaster = None
        bitting = None
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        num_padding = len(str(self.number_changes))
        num = 1
        rm_num = 1
        bm_num = 1
        num_letters = int(log(self.number_masters, self.kBA_length))
        a = 0
        b = 0
        c = 0
        d = 0
        psm_blind_code = ''
        pgm_blind_code = ''
        pbm_blind_code = ''
        pm_blind_code = ''
        bulk_bitting_add = []
        bulk_pm_add = []
        bulk_rm_add = []
        bulk_bm_add = []
        bulk_pbm_add = []
        bulk_pgm_add = []
        bulk_psm_add = []

        xBitting, xTopPin, xBotPin, state = self.build_bittings(self.ggmk)
        ggmk_str_bitting = ""
        for cut in self.ggmk:
            ggmk_str_bitting += str(cut)
        greatGrandMasterKey = {
            "id":uuid.uuid4(),
            "blind_code":"GGMK", 
            "bitting":ggmk_str_bitting, 
            "top_pin":xTopPin, 
            "bottom_pin":xBotPin, 
            "state":state, 
            "master_key_system":self.id,
            "great_grand_master":None,
            "row_master":None, 
            "page_master":None, 
            "page_block_master":None, 
            "page_group_master":None, 
            "page_section_master":None, 
            "block_master":None, 
            "key_level":"Great Grand Master"
            }
        output_system.append(greatGrandMasterKey)

        for j in range(self.kBA_length**self.max_rotation):
            #Page Section Master
            if (self.number_changes*(self.kBA_length**3) < (self.kBA_length**self.max_rotation)):
                if j%(self.number_changes*(self.kBA_length**3)) == 0:
                    ##TODO: Build page group Master
                    psm = self.generate_page_section_master(j)
                    xBitting, xTopPin, xBotPin, state = self.build_bittings(psm)
                    psm_blind_code = letters[d]
                    d = d+1
                    c = 0
                    b = 0
                    a = 0
                    pageSectionMaster = {
                        "id":uuid.uuid4(),
                        "blind_code":psm_blind_code, 
                        "bitting":xBitting, 
                        "top_pin":xTopPin, 
                        "bottom_pin":xBotPin, 
                        "state":state, 
                        "master_key_system":self.id,
                        "great_grand_master":greatGrandMasterKey["id"],
                        "row_master":None, 
                        "page_master":None, 
                        "page_block_master":None, 
                        "page_group_master":None, 
                        "page_section_master":None, 
                        "block_master":None, 
                        "key_level":"Page Section Master"
                        }
                    output_system.append(pageSectionMaster)
                    #bulk_psm_add.append(pageSectionMaster)

            #Page Group Master
            if (self.number_changes*(self.kBA_length**2) < (self.kBA_length**self.max_rotation)):
                if j%(self.number_changes*(self.kBA_length**2)) == 0:
                    pgm = self.generate_page_group_master(j)
                    xBitting, xTopPin, xBotPin, state = self.build_bittings(pgm)
                    pgm_blind_code = psm_blind_code + letters[c]
                    c = c+1
                    b = 0
                    a = 0
                    pageGroupMaster = {
                        "id":uuid.uuid4(),
                        "blind_code":pgm_blind_code, 
                        "bitting":xBitting, 
                        "top_pin":xTopPin, 
                        "bottom_pin":xBotPin, 
                        "state":state, 
                        "master_key_system":self.id, 
                        "great_grand_master":greatGrandMasterKey["id"],
                        "row_master":None,
                        "page_master":None,
                        "page_block_master":None, 
                        "page_group_master":None, 
                        "page_section_master":pageSectionMaster["id"] if pageSectionMaster else None,
                        "block_master":None, 
                        "key_level":"Page Group Master"
                        }
                    output_system.append(pageGroupMaster)
                    #bulk_pgm_add.append(pageGroupMaster)

            #Page Block Master
            if (self.number_changes*self.kBA_length < (self.kBA_length**self.max_rotation)):
                if j%(self.number_changes*self.kBA_length) == 0:
                    pbm = self.generate_page_block_master(j)
                    xBitting, xTopPin, xBotPin, state = self.build_bittings(pbm)
                    pbm_blind_code = pgm_blind_code + letters[b]
                    b = b+1
                    a = 0
                    pageBlockMaster = {
                        "id":uuid.uuid4(),
                        "blind_code":pbm_blind_code, 
                        "bitting":xBitting, 
                        "top_pin":xTopPin, 
                        "bottom_pin":xBotPin, 
                        "state":state, 
                        "master_key_system":self.id,
                        "great_grand_master":greatGrandMasterKey["id"],
                        "row_master":None,
                        "page_master":None,
                        "page_block_master":None, 
                        "page_group_master":pageGroupMaster["id"] if pageGroupMaster else None,
                        "page_section_master":pageSectionMaster["id"] if pageSectionMaster else None,  
                        "block_master":None, 
                        "key_level":"Page Block Master"
                        }
                    output_system.append(pageBlockMaster)

            #Page Masters
            if j%self.number_changes == 0:
                pm = self.generate_page_master(j)
                xBitting, xTopPin, xBotPin, state = self.build_bittings(pm)
                pm_blind_code = pbm_blind_code + letters[a]
                a = a+1
                pageMaster = {
                    "id":uuid.uuid4(),
                    "blind_code":pm_blind_code, 
                    "bitting":xBitting, 
                    "top_pin":xTopPin, 
                    "bottom_pin":xBotPin, 
                    "state":state, 
                    "master_key_system":self.id, 
                    "great_grand_master":greatGrandMasterKey["id"],
                    "row_master":None,
                    "page_master":None,
                    "page_block_master":pageBlockMaster["id"] if pageBlockMaster else None, 
                    "page_group_master":pageGroupMaster["id"] if pageGroupMaster else None, 
                    "page_section_master":pageSectionMaster["id"] if pageSectionMaster else None,   
                    "block_master":None, 
                    "key_level":"Page Master"}
                output_system.append(pageMaster)
                #bulk_pm_add.append(pageMaster)
                num = 1
                rm_num = 1
                bm_num =1

            #Row Masters
            if j%(self.kBA_length**2) == 0:
                rm = self.generate_row_master(j)
                xBitting, xTopPin, xBotPin, state = self.build_bittings(rm)
                rm_blind_code = pm_blind_code + '-R' + str(rm_num).zfill(num_padding)
                rm_num = rm_num + 1
                rowMaster = {
                    "id":uuid.uuid4(),
                    "blind_code":rm_blind_code, 
                    "bitting":xBitting, 
                    "top_pin":xTopPin, 
                    "bottom_pin":xBotPin, 
                    "state":state, 
                    "master_key_system":self.id,
                    "great_grand_master":greatGrandMasterKey["id"],
                    "row_master":None,
                    "page_master":pageMaster["id"] if pageMaster else None,
                    "page_block_master":pageBlockMaster["id"] if pageBlockMaster else None,
                    "page_group_master":pageGroupMaster["id"] if pageGroupMaster else None,
                    "page_section_master":pageSectionMaster["id"] if pageSectionMaster else None,
                    "block_master":None,
                    "key_level":"Row Master"
                    }
                output_system.append(rowMaster)

            #Block Masters
            if j%(self.kBA_length) == 0:
                bm = self.generate_block_master(j)
                xBitting, xTopPin, xBotPin, state = self.build_bittings(bm)
                bm_blind_code = pm_blind_code + '-B' + str(bm_num).zfill(num_padding)
                bm_num = bm_num + 1
                blockMaster = {
                    "id":uuid.uuid4(),
                    "blind_code":bm_blind_code, 
                    "bitting":xBitting, 
                    "top_pin":xTopPin, 
                    "bottom_pin":xBotPin, 
                    "state":state, 
                    "master_key_system":self.id,
                    "great_grand_master":greatGrandMasterKey["id"],
                    "row_master":rowMaster["id"] if rowMaster else None,
                    "page_master":pageMaster["id"] if pageMaster else None,
                    "page_block_master":pageBlockMaster["id"] if pageBlockMaster else None,
                    "page_group_master":pageGroupMaster["id"] if pageGroupMaster else None,
                    "page_section_master":pageSectionMaster["id"] if pageSectionMaster else None,
                    "block_master":None, 
                    "key_level":"Block Master"
                    }
                output_system.append(blockMaster)
                #bulk_bm_add.append(blockMaster)

            #CHK
            chk = self.generate_chk(j)
            xBitting, xTopPin, xBotPin, state = self.build_bittings(chk)
            xBlindCode = pm_blind_code + '-' + str(num).zfill(num_padding)
            num = num+1
            bitting = {
                "id":uuid.uuid4(),
                "blind_code":xBlindCode, 
                "bitting":xBitting, 
                "top_pin":xTopPin, 
                "bottom_pin":xBotPin, 
                "state":state, 
                "master_key_system":self.id, 
                "great_grand_master":greatGrandMasterKey["id"],
                "row_master":rowMaster["id"] if rowMaster else None, 
                "page_master":pageMaster["id"] if pageMaster else None, 
                "page_block_master":pageBlockMaster["id"] if pageBlockMaster else None, 
                "page_group_master":pageGroupMaster["id"] if pageGroupMaster else None, 
                "page_section_master":pageSectionMaster["id"] if pageSectionMaster else None, 
                "block_master":blockMaster["id"] if blockMaster else None, 
                "key_level":"Change Key"
                }
            output_system.append(bitting)

        return output_system

# mk = MasterKeySystemGen([3,5,2,4,6,7], [1, 2, 3, 4, 5, 6], [[1, 3, 5, 6, 2, 4],[4, 5, 2, 3, 1, 6],[1, 2, 3, 4, 5, 6],[6, 4, 3, 5, 2, 1]], 6, 4, 16, 7)
# system_output = mk.build_iterator()
