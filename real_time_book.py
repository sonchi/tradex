import gdax, time
from globals import PRODUCTS


class RealTimeBooks():
  def __init__(self):
    self.books = dict()
    for p in PRODUCTS:
      order_book = gdax.OrderBook(product_id=p)
      order_book.start()
      self.books[p] = order_book
      time.sleep(1)
    # Wait for all books to be initialized
    for p,order_book in self.books.items():
      book = order_book.get_current_book()
      while book['sequence'] == -1:
        book = order_book.get_current_book()
        time.sleep(1)
      print('{} book initialized, sequence {}'.format(p, book['sequence']))

  def bids(self, product):
    #order_book = self.books[product].get_current_book()
    #return order_book['bids'][-1]
    global value
    done = False
    while not done:
      try:
        value = self.books[product].get_bid()
        done = False if value is None else True
      except AttributeError:
        continue
    return value

  def asks(self, product):
    #order_book = self.books[product].get_current_book()
    #return order_book['asks'][0]
    global value
    done = False
    while not done:
      try:
        value = self.books[product].get_ask()
        done = False if value is None else True
      except AttributeError:
        continue
    return value

if __name__ == '__main__':
  books = RealTimeBooks()
  while True:
    print('\n\n\n')
    for p in PRODUCTS:
      #[bid_price, bid_size, bid_order] = books.bids(p)
      #[ask_price, ask_size, asks_order] = books.asks(p)
      print('{} bid: {} ask: {}'.format(p, books.bids(p), books.asks(p)))

# order_book = gdax.OrderBook(product_id='BTC-USD')
# order_book.start()
# time.sleep(20)
# order_book.close()