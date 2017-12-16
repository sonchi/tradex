import threading

# Initialize the books for all products. We keep one book per product.
# Each book contains @capacity snapshots updated in a round-robin
# fashion by the BookWriter of the corresponding product.
# Each snapshot contains a 'bids' dictionary and an 'asks' dictionary
# initialized to empty lists.
#
# BOOKS = { 'BTC-USD' : [{bids : [[]], asks : [[]]},
#                        {bids : [[]], asks : [[]]},
#
#                         ...
#
#                        {bids : [[]], asks : [[]]}],
#
#           'LTC-USD' : [{bids : [[]], asks : [[]]},
#                        {bids : [[]], asks : [[]]},
#
#                         ...
#
#                        {bids : [[]], asks : [[]]}],
#
#           'ETH-USD' : [{bids : [[]], asks : [[]]},
#                        {bids : [[]], asks : [[]]},
#
#                         ...
#
#                        {bids : [[]], asks : [[]]}],
#
#           'ETH-BTC' : [{bids : [[]], asks : [[]]},
#                        {bids : [[]], asks : [[]]},
#
#                         ...
#
#                        {bids : [[]], asks : [[]]}],
#
#           'LTC-BTC' : [{bids : [[]], asks : [[]]},
#                        {bids : [[]], asks : [[]]},
#
#                         ...
#
#                        {bids : [[]], asks : [[]]}] }
def init_books(products, capacity):
  books = dict()
  for p in products:
    books[p] = list()
    for i in range(capacity):
      books[p].append({'bids': [[]], 'asks': [[]]})
    assert len(books[p]) == capacity
  assert len(books) == len(products)
  return books

# BOOK_INDEX maps a product to the index of the most up-to-date snapshot in the list.
# The value is stored in a list to pass it by reference to BookWriter instances.
#
# Suppose
#   BOOK_INDEX['BTC-USD'] == [5] , then
#   BOOKS['BTC-USD'][5]
# contains the most up-to-date snapshot for 'BTC-USD'.
#
# BOOK_INDEX = { 'BTC-USD' : [-1],
#                'LTC-USD' : [-1],
#                'ETH-USD' : [-1],
#                'LTC-BTC' : [-1],
#                'ETH-BTC' : [-1] }
def init_book_index(products):
  book_index = dict()
  for p in products:
    book_index[p] = [-1]
  assert len(book_index) == len(products)
  return book_index

# Initialize locks. We keep one lock per product for synchronizing access to book_index.
def init_locks(products):
  locks = dict()
  for p in products:
    locks[p] = threading.Lock()
  return locks

BOOK_CAPACITY = 16

PRODUCTS = ['BTC-USD', 'LTC-USD', 'ETH-USD', 'ETH-BTC', 'LTC-BTC']

BOOKS = init_books(PRODUCTS, BOOK_CAPACITY)

BOOK_INDEX = init_book_index(PRODUCTS)

LOCKS = init_locks(PRODUCTS)