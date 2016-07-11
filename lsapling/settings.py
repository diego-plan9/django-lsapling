from django.conf import settings

LSAPLING_ORDERER_ADAPTER = getattr(
    settings,
    'LSAPLING_ORDERER_ADAPTER',
    'lsapling.ordering.simplebinaryorderer.SimpleBinaryOrdererAdapter')
