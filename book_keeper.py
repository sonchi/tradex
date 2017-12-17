import gdax
import json
import threading
import time
from globals import BOOKS, BOOK_CAPACITY, BOOK_INDEX, LOCKS, PRODUCTS

class BookWriter(threading.Thread):
  def __init__(self, product, books, book_index, locks):
    threading.Thread.__init__(self)
    self.daemon = True
    self.product = product
    assert type(locks) == dict
    self.lock = locks[self.product]
    assert type(books) == dict
    self.book = books[self.product]
    assert type(self.book) == list
    assert type(book_index) == dict
    self.book_index = book_index[self.product]
    assert type(self.book_index) == list
    assert len(self.book_index) == 1
    self.public_client = gdax.PublicClient()

  def run(self):
    exceed_count = 0
    update_count = 0
    while True:
      try:
        book = self.public_client.get_product_order_book(self.product, level=1)
      except (json.decoder.JSONDecodeError, ValueError) as e:
        continue
      if 'message' in book:
        # linear back off
        exceed_count = exceed_count + 1
        time.sleep(0.5 * exceed_count)
        # print('{} exceeded limits, update count:{}, exceed_count:{}'.format(self.product, update_count, exceed_count))
        continue
      else:
        exceed_count = 0
      # Increment the index, this is the index of the book that we are updating.
      index_ = (self.book_index[0] + 1) % BOOK_CAPACITY
      # print('Updating {} for {}'.format(index_, self.product))
      # Update the book at index_
      self.book[index_]['bids'] = book['bids'].copy()
      self.book[index_]['asks'] = book['asks'].copy()
      # Update the shared book index
      with self.lock:
        self.book_index[0] = index_
      update_count = update_count + 1

class BookReader():
  def __init__(self):
    # Warm up for book keepers
    time.sleep(5)

  def bid(self, product):
    with LOCKS[product]:
      index_ = BOOK_INDEX[product][0]
    return BOOKS[product][index_]['bids']

  def ask(self, product):
    with LOCKS[product]:
      index_ = BOOK_INDEX[product][0]
    return BOOKS[product][index_]['asks']

# if __name__ == '__main__':
#   writers = list()
#   for p in PRODUCTS:
#     w = BookWriter(p, BOOKS, BOOK_INDEX, LOCKS)
#     writers.append(w)
#   for w in writers:
#     w.start()
#   r = BookReader()
#   while True:
#     time.sleep(1)
#     for p in PRODUCTS:
#       print('\n\n{}'.format(p))
#       print('\n\nbids \n\n {}'.format(r.bid(p)))
#       print('\n\nasks \n\n {}'.format(r.ask(p)))