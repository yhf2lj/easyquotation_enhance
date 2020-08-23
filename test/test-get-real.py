from easyquotation_enhance import SinaQuotation

if __name__ == '__main__':
    dl_sina = SinaQuotation()
    print(dl_sina.get_real(['sh515700', 'sz000001']))
