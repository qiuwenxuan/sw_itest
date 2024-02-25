class GetNetworkInterfaceError(Exception):
    def __init__(self, message):
        # ���ø���Ĺ��캯�������ݴ�����Ϣ
        super().__init__(message)
        self.error_code = 101  # ��������Զ���Ĵ������


class GetVirtioBlkError(Exception):
    def __init__(self, message):
        # ���ø���Ĺ��캯�������ݴ�����Ϣ
        super().__init__(message)
        self.error_code = 102  # ��������Զ���Ĵ������


class ENVError(Exception):
    def __init__(self, message):
        # ���ø���Ĺ��캯�������ݴ�����Ϣ
        super().__init__(message)
        self.error_code = 103  # ��������Զ���Ĵ������


class Error(Exception):
    def __init__(self, message):
        # ���ø���Ĺ��캯�������ݴ�����Ϣ
        super().__init__(message)
        self.error_code = 104  # ��������Զ���Ĵ������


class TYPEError(Exception):
    def __init__(self, message):
        # ���ø���Ĺ��캯�������ݴ�����Ϣ
        super().__init__(message)
        self.error_code = 105  # ��������Զ���Ĵ������