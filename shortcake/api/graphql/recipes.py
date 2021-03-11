from __future__ import annotations

from typing import List

import strawberry

from shortcake.api.graphql.ingredients import Ingredient
from shortcake.database.models.recipes import Recipe as DBRecipe
from shortcake.database.models.recipes import RecipeIngredient as DBRecipeIngredient


@strawberry.type
class Recipe:
    id: strawberry.ID
    name: str
    description: str
    ingredients: List[RecipeIngredient]

    @classmethod
    def get_recipe(cls, id: strawberry.ID) -> Recipe:
        # Note: id shadows a builtin until either of the following are solved:
        # https://github.com/strawberry-graphql/strawberry/issues/727
        # https://github.com/strawberry-graphql/strawberry/issues/725
        db_recipe = DBRecipe.get_by_id(id)

        return cls.from_db_model(db_recipe)

    @classmethod
    def get_recipes(cls) -> List[Recipe]:
        db_recipes = DBRecipe.select()

        return list(map(cls.from_db_model, db_recipes))

    @classmethod
    def from_db_model(cls, db_recipe: DBRecipe) -> Recipe:
        return Recipe(
            id=db_recipe.id,
            name=db_recipe.name,
            description=db_recipe.description,
            ingredients=list(
                map(RecipeIngredient.from_db_model, db_recipe.ingredients)
            ),
        )


@strawberry.type
class RecipeIngredient:
    recipe: Recipe
    ingredient: Ingredient
    measurement: str
    modifier: str

    @classmethod
    def from_db_model(
        cls, db_recipe_ingredient: DBRecipeIngredient
    ) -> RecipeIngredient:
        return RecipeIngredient(
            recipe=db_recipe_ingredient.recipe,
            ingredient=Ingredient.get_ingredient(db_recipe_ingredient.ingredient),
            measurement=db_recipe_ingredient.measurement,
            modifier=db_recipe_ingredient.modifier,
        )
