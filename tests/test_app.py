import unittest
from app import app
from logic.nutriscore_calculator import calculate_nutriscore

class TestRandomRecipes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Client de test Flask
        self.app.testing = True

    def test_get_recipes_with_exact_match(self):
        # Exemple d'ingrédients saisis
        selected_ingredients = ["milk", "vanilla", "sugar"]

        # Ajout de chaque ingrédient un par un 
        for ingredient in selected_ingredients:
            self.app.post('/add_ingredient', json={'ingredient': ingredient})

        # requête POST pour obtenir des recettes avec les ingrédients exacts
        response = self.app.post('/get_recipes', 
                                 json={'exact_match': True, 'ingredients': selected_ingredients})

        self.assertEqual(response.status_code, 200)  # Vérification code de statut
        data = response.get_json()  # Récupératiin JSON de la réponse

        # Affichage des recettes retournées juste pour débogage
        print("Recettes retournées avec correspondance exacte :")
        for recipe in data:
            print(f"Title: {recipe['title']}")
            print(f"Ingredients: {recipe['ingredients']}")
            print("---g----g-----isma------------------")

        # Vérification des recettes qui contiennent exactement les ingrédients saisis
        for recipe in data:
            recipe_ingredients = [ingredient.lower().strip() for ingredient in recipe['ingredients']]  # Normalisation des ingrédients
            selected_ingredients_normalized = [ingredient.lower().strip() for ingredient in selected_ingredients]  # Normalisation des ingrédients saisis
            
            # On vérifie l'exactitude des ingrédients
            self.assertEqual(set(selected_ingredients_normalized), set(recipe_ingredients))  # Vérifie que les ingrédients sont exactement identiques

    def test_get_recipes_with_partial_match(self):
        # Le meme exemple d'ingrédients saisis plus haut pour confirmer le second test
        selected_ingredients = ["milk", "vanilla", "sugar"]

        # Ajout de chaque ingrédient un par un
        for ingredient in selected_ingredients:
            self.app.post('/add_ingredient', json={'ingredient': ingredient})

        # Requête POST pour obtenir des recettes avec des correspondances partielles
        response = self.app.post('/get_recipes', 
                                 json={'exact_match': False, 'ingredients': selected_ingredients})

        self.assertEqual(response.status_code, 200)  # Vérifie le code de statut
        data = response.get_json()  # Récupère le JSON de la réponse

        # Vérifie que les recettes contiennent au moins les ingrédients saisis, mais peuvent inclure d'autres
        for recipe in data:
            recipe_ingredients = [ingredient.lower().strip() for ingredient in recipe['ingredients']]  # Normalisation des ingrédients
            selected_ingredients_normalized = [ingredient.lower().strip() for ingredient in selected_ingredients]  # Normalisation des ingrédients saisis
            
            # Vérifiaction de la correspondance partielle
            self.assertTrue(all(ingredient in recipe_ingredients for ingredient in selected_ingredients_normalized))  # Vérifie une correspondance partielle

    def test_calculate_nutriscore(self):
        # Test case 1: High positive score
        ingredients = ['apple', 'spinach', 'chicken breast', 'quinoa', 'olive oil']
        expected_score = 'A'
        self.assertEqual(calculate_nutriscore(ingredients), expected_score)

        # Test case 2: Balanced score
        ingredients = ['apple', 'sugar', 'chicken breast', 'white bread', 'olive oil']
        expected_score = 'C'
        self.assertEqual(calculate_nutriscore(ingredients), expected_score)

        # Test case 3: High negative score
        ingredients = ['sugar', 'butter', 'white bread', 'processed cheese', 'bacon']
        expected_score = 'E'
        self.assertEqual(calculate_nutriscore(ingredients), expected_score)

        # Test case 4: Mixed score
        ingredients = ['apple', 'spinach', 'sugar', 'butter', 'olive oil']
        expected_score = 'C'
        self.assertEqual(calculate_nutriscore(ingredients), expected_score)

        # Test case 5: No ingredients
        ingredients = []
        expected_score = 'C'
        self.assertEqual(calculate_nutriscore(ingredients), expected_score)
          

if __name__ == '__main__':
    unittest.main()