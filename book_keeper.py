import gdax
import threading
import time
import random
from globals import BOOKS, BOOK_CAPACITY
from globals import BOOK_INDEX
from globals import PRODUCTS
from globals import LOCKS


class BookKeeper(threading.Thread):
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
    while True:
      book = self.public_client.get_product_order_book(self.product, level=2)
      if 'message' in book:
        exceed_count = exceed_count + 1
        print('{} XXXXXX {}'.format(self.product, exceed_count))
        time.sleep(0.5 * exceed_count)
        continue
      else:
        exceed_count = 0
      # Increment the index, this is the index of the book that we are updating.
      index_ = (self.book_index[0] + 1) % BOOK_CAPACITY
      #print('Updating {} for {}'.format(index_, self.product))
      # Update the book at index_
      self.book[index_]['bids'] = book['bids'].copy()
      self.book[index_]['asks'] = book['asks'].copy()
      # Update the shared book index.
      with self.lock:
        self.book_index[0] = index_

class BookReader(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.daemon = True
    # Warm up for book keepers
    time.sleep(5)

  def run(self):
    while True:
      print('\n\n')
      for p in PRODUCTS:
        index_ = -1
        with LOCKS[p]:
          index_ = BOOK_INDEX[p][0]
        print('{} index {}'.format(p, index_))
      print('\n\n')
      time.sleep(1)


if __name__ == '__main__':
  thread_list = list()
  for p in PRODUCTS:
    t = BookKeeper(p, BOOKS, BOOK_INDEX, LOCKS)
    thread_list.append(t)
  for t in thread_list:
    t.start()
  r = BookReader()
  r.start()
  while True:
    time.sleep(1)
