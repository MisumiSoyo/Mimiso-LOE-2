include "units.xs";



void CorvinianArmyApplier(int playerId = -1, int ObjectID = -1)
{
    int ObjectGoldCost = xsGetObjectAttribute(playerId, ObjectID, cGoldCost);
    ModAttribute(playerId, ObjectID, cFoodCost, ObjectGoldCost);
    SetAttribute(playerId, ObjectID, cGoldCost, 0);
}



void DetinetsObjectApplier(int playerId = -1, int ObjectID = -1)
{
    int ObjectStoneDiscount = xsGetObjectAttribute(playerId, ObjectID, cStoneCost) * 0.4;
    ModAttribute(playerId, ObjectID, cWoodCost, ObjectStoneDiscount);
    ModAttribute(playerId, ObjectID, cStoneCost, 0 - ObjectStoneDiscount);
}



void DetinetsTechApplier(int playerId = -1, int TechID = -1)
{
    int TechStoneDiscount = xsGetTechAttribute(playerId, TechID, cTechCost, cStoneCost) * 0.4;
    xsEffectAmount(cModifyTech, TechID, cAttrAddWoodCost, TechStoneDiscount, playerId);
    xsEffectAmount(cModifyTech, TechID, cAttrAddStoneCost, 0 - TechStoneDiscount, playerId);
}