from django.test import TestCase


class Test1(TestCase):

    def test_init(self):
        # Arrange



        # Act
        response = self.client.get(path='/gmod/')


        #Assert
        self.assertTemplateUsed(response, 'gmod/gmod.html')