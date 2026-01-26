## Code Snippets

- **createVariantScript.py**: creates a variant using complete USD files from Pixar's kitchen set
- **createVariantScriptDaCube.py** creates two variant sets for color and size for the mesh from carefully curated USD files. These files are curated in such a way that the variant part being changed in two files is not in the files for the other variant in order to "mix and match" them. Uses TestData/daCube 
- **createVariantScriptDaCube2.py**: creates two variant sets for color and size for a mesh using a script. "Mix and match" is possible
- **createTransformationVariantSet.py** allows setting up transformation variants. uses a script to record what changes were made and adds an additional xformOpOrder to account for other transformations 