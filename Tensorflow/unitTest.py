#
#  created by OFShare on 2019-05-30
#

import tensorflow as tf

class SquareTest(tf.test.TestCase):
    def testSquare(self):
        with self.test_session():
            print('Acui test')
            x = tf.square([2, 3])
            self.assertAllEqual(x.eval(), [4, 9])

if __name__ == "__main__":
    tf.test.main()
