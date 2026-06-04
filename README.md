## Maya USD Variant Author Toolkit

An open-source custom shelf to support variant authoring within Maya. Tools available within toolkit shelf:

<table border="0">
<tr>

<td valign="top">
<table>
<tr valign="middle">
<td><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/ModelVariant_AIcon.png" width="50px"></td>
<td>Modeling Variant Manager</td>
</tr>
<tr valign="middle">
<td><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/TransformVariant_AIcon.png" width="50px"></td>
<td>Transform Variant Manager</td>
</tr>
<tr valign="middle">
<td><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/MaterialVariant_AIcon.png" width="50px"></td>
<td>Material Variant Manager</td>
</tr>
</table>
</td>
  
<td valign="top">
<img width="500" alt="ToolkitVisualOptimized" src="https://github.com/user-attachments/assets/333e6014-30b2-4f56-bda2-6831e16547bd" />
</td>

</tr>
</table>

Toolkit Demo: https://www.youtube.com/watch?v=TzI132NprEA

## Installation
1. Download and unzip this repository in a location of your choosing
2. With an opened Maya scene, open the Script Editor
3. Click on 'File', and from the dropdown list, select 'Open Script'
4. With the Load Script dialog opened, locate the unzipped folder
5. Click into the folder, and then select the install.py file
6. Click 'Open' - the install.py script will be loaded into the Script Editor
7. Click the blue run button (▶) at the top of the Script Editor to run the script
8. When a dialog opens again, ensure you are inside the unzipped folder and click 'Save'
9. The Maya_USD_Variant_Author_Toolkit should be loaded into a shelf

## Documentation
[DOCUMENTATION | Maya-USD-Variant-Author-Toolkit](https://docs.google.com/document/d/1ipKrDLCjgtbGJnS1Inhu1NR4tvY33CLJlLu5xJTuQ54/edit?usp=sharing)

## Toolkit Walkthrough: Demo Project
Learn how to use this toolkit step-by-step! Beginner-friendly for USD users and those with limited Maya experience.
- Written version: [WALKTHROUGH | Maya USD Variant Author Toolkit](https://docs.google.com/document/d/1s75NcT0jil2NYX_dR0RY3g7EMvloyraf9dzsZMUVQ-M/edit?usp=sharing)
- Video version: [VIDEO WALKTHROUGH | Maya USD Variant Author Toolkit](https://youtu.be/g_c-OypIcpw?si=4LpFAuWirQQp4fr_)

## Troubleshooting
<table>
  <tr valign="middle">
     <td width="180">
      🛠️ TOOL(S)
    </td>
    <td>
      🐛 ISSUE 
    </td>
    <td>
      ✅ FIX 
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/ModelVariant_AIcon.png" width="50px">
    </td>
    <td>
     Instead of smoothed version, unsmoothed version of in-scene model used for modeling variant
    </td>
    <td>
      <ul>
        <li>Permanently smooth the in-scene model before assigning it to the variant</li> 
        <li>For further details on this, see Documentation</li>
      </ul>
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/TransformVariant_AIcon.png" width="50px">
    </td>
    <td>
     Unexpected transform applied when transform variant created on prim with USD reference
    </td>
    <td>
      <ul>
        <li>Referenced USD asset should be exported from (0,0,0) with transforms frozen and history deleted</li> 
      </ul>
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/TransformVariant_AIcon.png" width="50px">
    </td>
    <td>
      When attempting to create another transform variant set on the target prim, transformations seem "locked" in the viewport
    </td>
    <td>
      <ul>
        <li>You should only be creating multiple transform variant sets on the target prim if you are planning on separating its translations, rotations and scaling into different variant sets</li>
        <li>This issue will most commonly occur if the target prim has been translated from its original position, either when created or referenced</li>
          <li>In the case of translation, create a variant set for translation. For example, variant set "Location" with variants "Default" and "SceneLocation"</li>
      </ul>
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/MaterialVariant_AIcon.png" width="50px">
    </td>
    <td>
      Prim material not applied/changed after creating/toggling variants
    </td>
    <td>
      <ul>
        <li>In LookdevX, ensure that the image nodes for each material in the variant set are pointing to the right path in sourceimages/</li> 
        <li>With the prim selected, set 'Strength' in the attribute editor to 'Stronger than descendants'</li>
      </ul>
    </td>
  </tr>
</table>

## Limitations
<table>
  <tr valign="middle">
     <td width="180">
      🛠️ TOOL(S)
    </td>
    <td>
      🚧 LIMITATION 
    </td>
    <td>
      🔍 DETAILS & WORKAROUND
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/TransformVariant_AIcon.png" width="50px"><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/MaterialVariant_AIcon.png" width="50px">
    </td>
    <td>
      Editing Variant Sets & Variants
    </td>
    <td>
      <ul>
        <li>For these 2 tools, variants are created individually and one at a time for the variant set rather than all at once (for further details, see Documentation)</li>
        <li>There is no support to be able to immediately edit a variant or variant set right after its creation</li>
        <li>To edit, the tool must be closed and reopened for the same prim/Xform</li>
        <li>This  limitation applies even while editing, when creating a new variant within an existing variant set</li>
      </ul>
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/ModelVariant_AIcon.png" width="50px"><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/TransformVariant_AIcon.png" width="50px"><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/MaterialVariant_AIcon.png" width="50px">
    </td>
    <td>
      Undo Action
    </td>
    <td>
      <ul>
        <li>Currently, there is no support to undo an action that was taken using the toolkit</li> 
          <li>However, it is possible to edit a variant set. This includes: deleting the variant set, deleting a variant in the set, and adding a new variant to an existing set</li>
          <li>For further help on editing variant sets, see Documentation</li>
      </ul>
    </td>
  </tr>
  <tr valign="middle">
    <td>
      <img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/ModelVariant_AIcon.png" width="50px"><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/TransformVariant_AIcon.png" width="50px"><img src="https://github.com/nMDaas/USD_Switchboard/blob/main/icons/MaterialVariant_AIcon.png" width="50px">
    </td>
    <td>
      Removing Variant Entry Rows
    </td>
    <td>
      <ul>
        <li>Currently, there is no support to remove a variant entry row after it has been created</li> 
        <li>However, based on the tool, this is managed:</li> 
        <ul>
          <li>Modeling Variant Manager: If an entry row for a variant has no information attached to it, the entry row is ignored when 'Create Variants' is clicked</li>
          <li>Transform & Material Variant Manager: Since variants are created individually, an entry row that is no longer needed can be ignored by simply not creating the variant. See Documentation for more details</li>
        </ul>
      </ul>
    </td>
  </tr>
</table>

## Contributing
This project is open source, and contributions are welcome! If there are features/improvements you’d like to see or bugs that need fixing, feel free to open a pull request.

## Further Questions/Comments/Concerns?
For additional questions, troubleshooting help, bugs or errors, feel free to create an issue on GitHub or contact Natasha Daas on [LinkedIn](https://www.linkedin.com/in/natashamishradaas/)


## Credits
- Folder icons created by kmg design - Flaticon
- Files and folders icons created by Gajah Mada - Flaticon
- Dirrection icons created by popcic - Flaticon
- Warning icons created by Rakib Hassan Rahim - Flaticon
- Pointer icons created by Amazona Adorada - Flaticon
- Cursor icons created by Freepik - Flaticon
