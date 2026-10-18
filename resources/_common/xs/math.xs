//  Math functions


bool isClassID(int id = -1)
{
    return ((id >= 900) && (id <= 964));
}

int minInt(int a = 0, int b = 0)
{
    if (a<b)
        return (a);
    return (b);
}


int maxInt(int a = 0, int b = 0)
{
    if (a<b)
        return (b);
    return (a);
}

float minFloat(float a = 0.0, float b = 0.0)
{
    if (a<b)
        return (a);
    return (b);
}


float maxFloat(float a = 0.0, float b = 0.0)
{
    if (a<b)
        return (b);
    return (a);
}


int BitwiseRemove(int a = 0, int b = 0)
{
    return (bitAnd(a, bitNot(b)));
}


float DistanceX(vector posa = vector(-1.0, -1.0, -1.0), vector posb = vector(-1.0, -1.0, -1.0))
{
    return (abs(xsVectorGetX(posa)-xsVectorGetX(posb)));
}


float DistanceY(vector posa = vector(-1.0, -1.0, -1.0), vector posb = vector(-1.0, -1.0, -1.0))
{
    return (abs(xsVectorGetY(posa)-xsVectorGetY(posb)));
}


float Distance(vector posa = vector(-1.0, -1.0, -1.0), vector posb = vector(-1.0, -1.0, -1.0))
{
    return (sqrt(pow(xsVectorGetX(posa)-xsVectorGetX(posb), 2)+pow(xsVectorGetY(posa)-xsVectorGetY(posb), 2)));
}


//  Manhattan Distance
float MDistance(vector posa = vector(-1.0, -1.0, -1.0), vector posb = vector(-1.0, -1.0, -1.0))
{
    return (abs(xsVectorGetX(posa)-xsVectorGetX(posb))+abs(xsVectorGetY(posa)-xsVectorGetY(posb)));
}


void PrintMessage(string Message = "")
{
    static int MessageNum = 0;
    xsChatData("Message " + MessageNum + ": " + Message);
    MessageNum ++;
}


bool RandomChance(int Chance = 0)
{
    int tmp = xsGetRandomNumberLH(0, 100) + 1;
    return (tmp <= Chance);
}


bool isAlly(int player1 = -1, int player2 = -1)
{
    return (xsGetDiplomacy(player1, player2) == cDiplomacyAlly);
}

bool isEnemy(int player1 = -1, int player2 = -1)
{
    return (xsGetDiplomacy(player1, player2) == cDiplomacyEnemy);
}


bool isResearched(int playerId = -1, int TechID = -1)
{
    return (xsGetTechState(TechID, playerId) == cTechStateDone);
}


void EnableObject(int playerId = -1, int ObjectID = -1)
{
    xsEffectAmount(cEnableObject, ObjectID, 1, 0, playerId);
}


void DisableObject(int playerId = -1, int ObjectID = -1)
{
    xsEffectAmount(cEnableObject, ObjectID, 0, 0, playerId);
}


void SetTechAuto(int playerId = -1, int TechID = -1)
{
    xsEffectAmount(cModifyTech, TechID, cAttrSetTime, 0, playerId);
    xsEffectAmount(cModifyTech, TechID, cAttrMulAllCosts, 0, playerId);
}


void EnableTech(int playerId = -1, int TechID = -1)
{
    xsEffectAmount(cModifyTech, TechID, cAttrSetState, cAttributeEnable, playerId);
}


void DisableTech(int playerId = -1, int TechID = -1)
{
    xsEffectAmount(cDisableTech, TechID, 0, 0, playerId);
}


void ForceEnableTech(int playerId = -1, int TechID = -1)
{
    xsEffectAmount(cModifyTech, TechID, cAttrSetState, cAttributeForce, playerId);
}


void ForceResearchTech(int playerId = -1, int TechID = -1, bool SetAuto = false)
{
    if (isResearched(playerId, TechID) == false)
    {
        xsEffectAmount(cModifyTech, TechID, cAttrSetState, cAttributeResearch, playerId);
        if (SetAuto)
            xsEffectAmount(cModifyTech, TechID, cAttrSetTime, 0, playerId);
    }
}


void SetTechStack(int playerId = -1, int TechID = -1, int ResearchCap = 1)
{
    xsEffectAmount(cModifyTech, TechID, cAttrSetStacking, 1, playerId);
    xsEffectAmount(cModifyTech, TechID, cAttrSetStackingResearchCap, ResearchCap, playerId);
}


void SetAttribute(int playerId = -1, int ObjectID = -1, int AttributeID = -1, float value = -1)
{
    xsEffectAmount(cSetAttribute, ObjectID, AttributeID, value, playerId);
}


void ModAttribute(int playerId = -1, int ObjectID = -1, int AttributeID = -1, float value = -1)
{
    xsEffectAmount(cAddAttribute, ObjectID, AttributeID, value, playerId);
}


void MulAttribute(int playerId = -1, int ObjectID = -1, int AttributeID = -1, float value = -1)
{
    xsEffectAmount(cMulAttribute, ObjectID, AttributeID, value, playerId);
}


void SetAttack(int playerId = -1, int ObjectID = -1, int DamageClass = -1, int value = -1)
{
    if  (value > 0)
        xsEffectAmount(cSetAttribute, ObjectID, cAttack, DamageClass * 256 + value, playerId);
    else
        xsEffectAmount(cSetAttribute, ObjectID, cAttack, 0 - DamageClass * 256 + value, playerId);
}


void SetArmor(int playerId = -1, int ObjectID = -1, int DamageClass = -1, int value = -1)
{
    if  (value > 0)
        xsEffectAmount(cSetAttribute, ObjectID, cArmor, DamageClass * 256 + value, playerId);
    else
        xsEffectAmount(cSetAttribute, ObjectID, cArmor, 0 - DamageClass * 256 + value, playerId);
}


void ModAttack(int playerId = -1, int ObjectID = -1, int DamageClass = -1, int value = -1)
{
    if  (value > 0)
        xsEffectAmount(cAddAttribute, ObjectID, cAttack, DamageClass * 256 + value, playerId);
    else
        xsEffectAmount(cAddAttribute, ObjectID, cAttack, 0 - DamageClass * 256 + value, playerId);
}


void ModAttackBonus(int playerId = -1, int ClassTarget = -1, float value = 0.0)
{
    ModAttack(playerId, ClassTarget, cDamageClassInfantry, value);
    ModAttack(playerId, ClassTarget, cDamageClassElephantUnits, value);
    ModAttack(playerId, ClassTarget, cDamageClassCavalry, value);
    ModAttack(playerId, ClassTarget, cDamageClassArchers, value);
    ModAttack(playerId, ClassTarget, cDamageClassAllBuildings, value);
    ModAttack(playerId, ClassTarget, cDamageClassStoneDefense, value);
    ModAttack(playerId, ClassTarget, cDamageClassPredatorAnimals, value);
    ModAttack(playerId, ClassTarget, cDamageClassShips, value);
    ModAttack(playerId, ClassTarget, cDamageClassRams, value);
    ModAttack(playerId, ClassTarget, cDamageClassUniqueUnits, value);
    ModAttack(playerId, ClassTarget, cDamageClassSiegeWeapons, value);
    ModAttack(playerId, ClassTarget, cDamageClassStandardBuildings, value);
    ModAttack(playerId, ClassTarget, cDamageClassGunpowderUnits, value);
    ModAttack(playerId, ClassTarget, cDamageClassMonks, value);
    ModAttack(playerId, ClassTarget, cDamageClassCastles, value);
    ModAttack(playerId, ClassTarget, cDamageClassSpearmen, value);
    ModAttack(playerId, ClassTarget, cDamageClassCavalryArchers, value);
    ModAttack(playerId, ClassTarget, cDamageClassShockInfantry, value);
    ModAttack(playerId, ClassTarget, cDamageClassCamelUnits, value);
    ModAttack(playerId, ClassTarget, cDamageClassFishingShips, value);
    ModAttack(playerId, ClassTarget, cDamageClassMamelukes, value);
    ModAttack(playerId, ClassTarget, cDamageClassHeroesAndKings, value);
    ModAttack(playerId, ClassTarget, cDamageClassHeavySiege, value);
    ModAttack(playerId, ClassTarget, cDamageClassSkirmishers, value);
}


void ModArmor(int playerId = -1, int ObjectID = -1, int DamageClass = -1, int value = -1)
{
    if  (value > 0)
        xsEffectAmount(cAddAttribute, ObjectID, cArmor, DamageClass * 256 + value, playerId);
    else
        xsEffectAmount(cAddAttribute, ObjectID, cArmor, 0 - DamageClass * 256 + value, playerId);
}


void MulAttack(int playerId = -1, int ObjectID = -1, int DamageClass = -1, float value = -1)
{
    if (value > 0)
        xsEffectAmount(cMulAttribute, ObjectID, cAttack, value * 100 + DamageClass * 256, playerId);
    else
        xsEffectAmount(cMulAttribute, ObjectID, cAttack, 0.0 - value * 256 + DamageClass * 100, playerId);
}


void MulAttackBonus(int playerId = -1, int ClassTarget = -1, float value = 0.0)
{
    MulAttack(playerId, ClassTarget, cDamageClassInfantry, value);
    MulAttack(playerId, ClassTarget, cDamageClassElephantUnits, value);
    MulAttack(playerId, ClassTarget, cDamageClassCavalry, value);
    MulAttack(playerId, ClassTarget, cDamageClassArchers, value);
    MulAttack(playerId, ClassTarget, cDamageClassAllBuildings, value);
    MulAttack(playerId, ClassTarget, cDamageClassStoneDefense, value);
    MulAttack(playerId, ClassTarget, cDamageClassPredatorAnimals, value);
    MulAttack(playerId, ClassTarget, cDamageClassShips, value);
    MulAttack(playerId, ClassTarget, cDamageClassRams, value);
    MulAttack(playerId, ClassTarget, cDamageClassUniqueUnits, value);
    MulAttack(playerId, ClassTarget, cDamageClassSiegeWeapons, value);
    MulAttack(playerId, ClassTarget, cDamageClassStandardBuildings, value);
    MulAttack(playerId, ClassTarget, cDamageClassGunpowderUnits, value);
    MulAttack(playerId, ClassTarget, cDamageClassMonks, value);
    MulAttack(playerId, ClassTarget, cDamageClassCastles, value);
    MulAttack(playerId, ClassTarget, cDamageClassSpearmen, value);
    MulAttack(playerId, ClassTarget, cDamageClassCavalryArchers, value);
    MulAttack(playerId, ClassTarget, cDamageClassShockInfantry, value);
    MulAttack(playerId, ClassTarget, cDamageClassCamelUnits, value);
    MulAttack(playerId, ClassTarget, cDamageClassFishingShips, value);
    MulAttack(playerId, ClassTarget, cDamageClassMamelukes, value);
    MulAttack(playerId, ClassTarget, cDamageClassHeroesAndKings, value);
    MulAttack(playerId, ClassTarget, cDamageClassHeavySiege, value);
    MulAttack(playerId, ClassTarget, cDamageClassSkirmishers, value);
    MulAttack(playerId, ClassTarget, 60, value);
}


void MulArmor(int playerId = -1, int ObjectID = -1, int DamageClass = -1, float value = -1)
{
    if (value > 0)
        xsEffectAmount(cMulAttribute, ObjectID, cArmor, value * 100 + DamageClass * 256, playerId);
    else
        xsEffectAmount(cMulAttribute, ObjectID, cArmor, 0.0 - value * 256 + DamageClass * 100, playerId);
}


void SetResource(int playerId = -1, int ResourceID = -1, float value = 0.0)
{
    xsEffectAmount(cModResource, ResourceID, 0, value, playerId);
}


void ModResource(int playerId = -1, int ResourceID = -1, float value = 0.0)
{
    xsEffectAmount(cModResource, ResourceID, 1, value, playerId);
}


void MulResource(int playerId = -1, int ResourceID = -1, float value = 0.0)
{
    xsEffectAmount(cMulResource, ResourceID, 0, value, playerId);
}


void SetAllyResource(int playerId = -1, int ResourceID = -1, float value = 0.0)
{
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if ((i == playerId) || (isAlly(playerId, i)))
            xsEffectAmount(cModResource, ResourceID, 0, value, i);
}


void ModAllyResource(int playerId = -1, int ResourceID = -1, float value = 0.0)
{
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if ((i == playerId) || (isAlly(playerId, i)))
            xsEffectAmount(cModResource, ResourceID, 1, value, i);
}


void MulAllyResource(int playerId = -1, int ResourceID = -1, float value = 0.0)
{
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if ((i == playerId) || (isAlly(playerId, i)))
            xsEffectAmount(cMulResource, ResourceID, 0, value, i);
}


void MulAllyAttribute(int playerId = -1, int ObjectID = -1, int AttributeID = -1, float value = 0.0)
{
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if ((i == playerId) || (isAlly(playerId, i)))
            xsEffectAmount(cMulAttribute, ObjectID, AttributeID, value, i);
}


void SpawnUnit(int playerId = -1, int SpawnUnitID = -1, int SpawnBuidingID = -1, int SpawnNum = -1, int SpawnBuildingCap = 0, bool isInside = false)
{
    xsEffectAmount(cModResource, cAttributeSpawnCap, 0, SpawnBuildingCap, playerId);
    if (isInside)
        xsEffectAmount(cModResource, cAttributeSpawnStayInside, 0, 1, playerId);
    xsEffectAmount(cSpawnUnit, SpawnUnitID, SpawnBuidingID, SpawnNum, playerId);
    xsEffectAmount(cModResource, cAttributeSpawnStayInside, 0, 0, playerId);
}


void UpgradeUnit(int playerId = -1, int SourceObject = -1, int TargetObject = -1, int UpgradeMode = 0)
{
    xsEffectAmount(cUpgradeUnit, SourceObject, TargetObject, UpgradeMode, playerId);
}


void LaunchAura(int playerId = -1, int ObjectID = -1, bool isSelf = false)
{
    int ObjectCombatAbility = 0;
    int tmp1 = 0;
    int tmp2 = 32;
    int PlayerObjectCount = xsGetPlayerNumberOfObjects(playerId);
    if (isSelf)
        tmp2 = 96;
    if ((ObjectID >= 900) && (ObjectID <= 964))
    {
        int i = 0;
        for (i = 0; < PlayerObjectCount)
            if (((i < 900) || (i > 964)) && (xsGetObjectClass(playerId, i) == ObjectID))
            {
                ObjectCombatAbility = xsGetObjectAttribute(playerId, i, cCombatAbility);
                tmp1 = bitOr(ObjectCombatAbility, tmp2);
                if (tmp1 != ObjectCombatAbility)
                    xsEffectAmount(cSetAttribute, i, cCombatAbility, tmp1, playerId);
            }
        return;
    }
    ObjectCombatAbility = xsGetObjectAttribute(playerId, ObjectID, cCombatAbility);
    ObjectCombatAbility = bitOr(ObjectCombatAbility, tmp2);
    xsEffectAmount(cSetAttribute, ObjectID, cCombatAbility, ObjectCombatAbility, playerId);
}


void RemoveAura(int playerId = -1, int ObjectID = -1)
{
    int ObjectCombatAbility = 0;
    int tmp1 = 0;
    int tmp2 = 96;
    int PlayerObjectCount = xsGetPlayerNumberOfObjects(playerId);
    if ((ObjectID >= 900) && (ObjectID <= 964))
    {
        int i = 0;
        for (i = 0; < PlayerObjectCount)
            if (((i < 900) || (i > 964)) && (xsGetObjectClass(playerId, i) == ObjectID))
            {
                ObjectCombatAbility = xsGetObjectAttribute(playerId, i, cCombatAbility);
                tmp1 = BitwiseRemove(ObjectCombatAbility, tmp2);
                if (tmp1 != ObjectCombatAbility)
                    xsEffectAmount(cSetAttribute, i, cCombatAbility, tmp1, playerId);
            }
        return;
    }
    ObjectCombatAbility = xsGetObjectAttribute(playerId, ObjectID, cCombatAbility);
    ObjectCombatAbility = BitwiseRemove(ObjectCombatAbility, tmp2);
    xsEffectAmount(cSetAttribute, ObjectID, cCombatAbility, ObjectCombatAbility, playerId);
}


void LaunchStinger(int playerId = -1, int ObjectID = -1)
{
    int ObjectCombatAbility = 0;
    int tmp1 = 0;
    int tmp2 = 128;
    int PlayerObjectCount = xsGetPlayerNumberOfObjects(playerId);
    if ((ObjectID >= 900) && (ObjectID <= 964))
    {
        int i = 0;
        for (i = 0; < PlayerObjectCount)
            if (((i < 900) || (i > 964)) && (xsGetObjectClass(playerId, i) == ObjectID))
            {
                ObjectCombatAbility = xsGetObjectAttribute(playerId, i, cCombatAbility);
                tmp1 = bitOr(ObjectCombatAbility, tmp2);
                if (tmp1 != ObjectCombatAbility)
                    xsEffectAmount(cSetAttribute, i, cCombatAbility, tmp1, playerId);
            }
        return;
    }
    ObjectCombatAbility = xsGetObjectAttribute(playerId, ObjectID, cCombatAbility);
    ObjectCombatAbility = bitOr(ObjectCombatAbility, tmp2);
    xsEffectAmount(cSetAttribute, ObjectID, cCombatAbility, ObjectCombatAbility, playerId);
}


void RemoveStinger(int playerId = -1, int ObjectID = -1)
{
    int ObjectCombatAbility = 0;
    int tmp1 = 0;
    int tmp2 = 128;
    int PlayerObjectCount = xsGetPlayerNumberOfObjects(playerId);
    if ((ObjectID >= 900) && (ObjectID <= 964))
    {
        int i = 0;
        for (i = 0; < PlayerObjectCount)
            if (((i < 900) || (i > 964)) && (xsGetObjectClass(playerId, i) == ObjectID))
            {
                ObjectCombatAbility = xsGetObjectAttribute(playerId, i, cCombatAbility);
                tmp1 = BitwiseRemove(ObjectCombatAbility, tmp2);
                if (tmp1 != ObjectCombatAbility)
                    xsEffectAmount(cSetAttribute, i, cCombatAbility, tmp1, playerId);
            }
        return;
    }
    ObjectCombatAbility = xsGetObjectAttribute(playerId, ObjectID, cCombatAbility);
    ObjectCombatAbility = BitwiseRemove(ObjectCombatAbility, tmp2);
    xsEffectAmount(cSetAttribute, ObjectID, cCombatAbility, ObjectCombatAbility, playerId);
}


int ObjectTotalCost(int playerId = -1, int ObjectID = -1)
{
    int Ans = 0;
    int i = 0;
    int cost = 0;
    for (i = cFoodCost; <= cStoneCost)
    {
        cost = xsGetObjectAttribute(playerId, ObjectID, i);
        if (cost > -1)
            Ans = Ans + cost;
    }
    return (Ans);
}


int roundToInt(float number = 0.0)
{
    int IntegerPart = floor(number);
    if (number - IntegerPart >= 0.5)
        return (IntegerPart + 1);
    return (IntegerPart);
}


void ApplyToAllMilitaryTargets(int playerId = -1, int ClassTarget = -1, int TaskType = -1, bool includeSiege = true)
{
    xsTask(ClassTarget, TaskType, cArcherClass, playerId);
    xsTask(ClassTarget, TaskType, cInfantryClass, playerId);
    xsTask(ClassTarget, TaskType, cCavalryClass, playerId);
    xsTask(ClassTarget, TaskType, cSiegeWeaponClass, playerId);
    xsTask(ClassTarget, TaskType, cMonkClass, playerId);
    xsTask(ClassTarget, TaskType, cTransportShipClass, playerId);
    xsTask(ClassTarget, TaskType, cWarshipClass, playerId);
    xsTask(ClassTarget, TaskType, cConquistadorClass, playerId);
    xsTask(ClassTarget, TaskType, cPhalanxClass, playerId);
    xsTask(ClassTarget, TaskType, cPetardClass, playerId);
    xsTask(ClassTarget, TaskType, cCavalryArcherClass, playerId);
    xsTask(ClassTarget, TaskType, cMonkWithRelicClass, playerId);
    xsTask(ClassTarget, TaskType, cHandCannoneerClass, playerId);
    xsTask(ClassTarget, TaskType, cScoutCavalryClass, playerId);
    xsTask(ClassTarget, TaskType, cLandMineClass, playerId);

    if (includeSiege)
    {
        xsTask(ClassTarget, TaskType, cSiegeWeaponClass, playerId);
        xsTask(ClassTarget, TaskType, cPackedUnitClass, playerId);
        xsTask(ClassTarget, TaskType, cUnpackedSiegeUnitClass, playerId);
        xsTask(ClassTarget, TaskType, cScorpionClass, playerId);
    }
}


void ApplyAllMilitaryToTarget(int playerId = -1, int ClassTarget = -1, int TaskType = -1, bool includeSiege = true, bool incMisc = false)
{
    xsTask(cArcherClass, TaskType, ClassTarget, playerId);
    xsTask(cInfantryClass, TaskType, ClassTarget, playerId);
    xsTask(cCavalryClass, TaskType, ClassTarget, playerId);
    xsTask(cSiegeWeaponClass, TaskType, ClassTarget, playerId);
    xsTask(cMonkClass, TaskType, ClassTarget, playerId);
    xsTask(cTransportShipClass, TaskType, ClassTarget, playerId);
    xsTask(cWarshipClass, TaskType, ClassTarget, playerId);
    xsTask(cConquistadorClass, TaskType, ClassTarget, playerId);
    xsTask(cPhalanxClass, TaskType, ClassTarget, playerId);
    xsTask(cPetardClass, TaskType, ClassTarget, playerId);
    xsTask(cCavalryArcherClass, TaskType, ClassTarget, playerId);
    xsTask(cMonkWithRelicClass, TaskType, ClassTarget, playerId);
    xsTask(cHandCannoneerClass, TaskType, ClassTarget, playerId);
    xsTask(cScoutCavalryClass, TaskType, ClassTarget, playerId);
    xsTask(cLandMineClass, TaskType, ClassTarget, playerId);

    if (includeSiege)
    {
        xsTask(cSiegeWeaponClass, TaskType, ClassTarget, playerId);
        xsTask(cPackedUnitClass, TaskType, ClassTarget, playerId);
        xsTask(cUnpackedSiegeUnitClass, TaskType, ClassTarget, playerId);
        xsTask(cScorpionClass, TaskType, ClassTarget, playerId);
    }

    if (incMisc)
    {
        xsTask(cMiscellaneousClass, TaskType, ClassTarget, playerId);
    }
}


void ApplyToAllPlayerTargets(int playerId = -1, int ClassTarget = -1, int TaskType = -1, bool includeBuildings = false, bool includeSiege = true, bool includeAnimals = false)
{
    xsTask(ClassTarget, TaskType, cArcherClass, playerId);
    xsTask(ClassTarget, TaskType, cTradeBoatClass, playerId);
    xsTask(ClassTarget, TaskType, cVillagerClass, playerId);
    xsTask(ClassTarget, TaskType, cInfantryClass, playerId);
    xsTask(ClassTarget, TaskType, cCavalryClass, playerId);
    xsTask(ClassTarget, TaskType, cMonkClass, playerId);
    xsTask(ClassTarget, TaskType, cTradeCartClass, playerId);
    xsTask(ClassTarget, TaskType, cTransportShipClass, playerId);
    xsTask(ClassTarget, TaskType, cFishingBoatClass, playerId);
    xsTask(ClassTarget, TaskType, cWarshipClass, playerId);
    xsTask(ClassTarget, TaskType, cConquistadorClass, playerId);
    xsTask(ClassTarget, TaskType, cPetardClass, playerId);
    xsTask(ClassTarget, TaskType, cCavalryArcherClass, playerId);
    xsTask(ClassTarget, TaskType, cMonkWithRelicClass, playerId);
    xsTask(ClassTarget, TaskType, cHandCannoneerClass, playerId);
    xsTask(ClassTarget, TaskType, cScoutCavalryClass, playerId);
    xsTask(ClassTarget, TaskType, cKingClass, playerId);
    xsTask(ClassTarget, TaskType, cLandMineClass, playerId);

    if (includeBuildings)
    {
        xsTask(ClassTarget, TaskType, cBuildingClass, playerId);
        xsTask(ClassTarget, TaskType, cGateClass, playerId);
        xsTask(ClassTarget, TaskType, cWallClass, playerId);
        xsTask(ClassTarget, TaskType, cTowerClass, playerId);
        xsTask(ClassTarget, TaskType, cFarmClass, playerId);
    }
    if (includeSiege)
    {
        xsTask(ClassTarget, TaskType, cSiegeWeaponClass, playerId);
        xsTask(ClassTarget, TaskType, cPackedUnitClass, playerId);
        xsTask(ClassTarget, TaskType, cUnpackedSiegeUnitClass, playerId);
        xsTask(ClassTarget, TaskType, cScorpionClass, playerId);
    }
    if (includeAnimals)
    {
        xsTask(ClassTarget, TaskType, cPreyAnimalClass, playerId);
        xsTask(ClassTarget, TaskType, cPredatorAnimalClass, playerId);
        xsTask(ClassTarget, TaskType, cDomesticAnimalClass, playerId);
        xsTask(ClassTarget, TaskType, cLivestockClass, playerId);
        xsTask(ClassTarget, TaskType, cControlledAnimalClass, playerId);
    }
}


void ApplyAllToTarget(int playerId = -1, int ClassTarget = -1, int TaskType = -1, bool includeBuildings = false, bool includeSiege = true, bool includeAnimals = false, bool incMisc = false)
{
    xsTask(cArcherClass, TaskType, ClassTarget, playerId);
    xsTask(cTradeBoatClass, TaskType, ClassTarget, playerId);
    xsTask(cVillagerClass, TaskType, ClassTarget, playerId);
    xsTask(cInfantryClass, TaskType, ClassTarget, playerId);
    xsTask(cCavalryClass, TaskType, ClassTarget, playerId);
    xsTask(cSiegeWeaponClass, TaskType, ClassTarget, playerId);
    xsTask(cMonkClass, TaskType, ClassTarget, playerId);
    xsTask(cTradeCartClass, TaskType, ClassTarget, playerId);
    xsTask(cTransportShipClass, TaskType, ClassTarget, playerId);
    xsTask(cFishingBoatClass, TaskType, ClassTarget, playerId);
    xsTask(cWarshipClass, TaskType, ClassTarget, playerId);
    xsTask(cConquistadorClass, TaskType, ClassTarget, playerId);
    xsTask(cPhalanxClass, TaskType, ClassTarget, playerId);
    xsTask(cPetardClass, TaskType, ClassTarget, playerId);
    xsTask(cCavalryArcherClass, TaskType, ClassTarget, playerId);
    xsTask(cMonkWithRelicClass, TaskType, ClassTarget, playerId);
    xsTask(cHandCannoneerClass, TaskType, ClassTarget, playerId);
    xsTask(cScoutCavalryClass, TaskType, ClassTarget, playerId);
    xsTask(cKingClass, TaskType, ClassTarget, playerId);
    xsTask(cLandMineClass, TaskType, ClassTarget, playerId);

    if (includeBuildings)
    {
        xsTask(cBuildingClass, TaskType, ClassTarget, playerId);
        xsTask(cGateClass, TaskType, ClassTarget, playerId);
        xsTask(cWallClass, TaskType, ClassTarget, playerId);
        xsTask(cTowerClass, TaskType, ClassTarget, playerId);
        xsTask(cFarmClass, TaskType, ClassTarget, playerId);
    }

    if (includeSiege)
    {
        xsTask(cSiegeWeaponClass, TaskType, ClassTarget, playerId);
        xsTask(cPackedUnitClass, TaskType, ClassTarget, playerId);
        xsTask(cUnpackedSiegeUnitClass, TaskType, ClassTarget, playerId);
        xsTask(cScorpionClass, TaskType, ClassTarget, playerId);
    }

    if (includeAnimals)
    {
        xsTask(cPreyAnimalClass, TaskType, ClassTarget, playerId);
        xsTask(cPredatorAnimalClass, TaskType, ClassTarget, playerId);
        xsTask(cDomesticAnimalClass, TaskType, ClassTarget, playerId);
        xsTask(cLivestockClass, TaskType, ClassTarget, playerId);
        xsTask(cControlledAnimalClass, TaskType, ClassTarget, playerId);
    }

    if (incMisc)
    {
        xsTask(cMiscellaneousClass, TaskType, ClassTarget, playerId);
    }
}


bool isInRange(int UnitID = -1, int ArrayID = -1, float Range = 0.0, bool isSquire = False)
{
    vector PosA = xsGetUnitPosition(UnitID);
    int i = 0;
    int ArraySize = xsArrayGetSize(ArrayID);
    for (i = 0; < ArraySize)
    {
        vector PosB = xsGetUnitPosition(xsArrayGetInt(ArrayID, i));
        if (isSquire)
        {
            if ((DistanceX(PosA, PosB) <= Range) && (DistanceY(PosA, PosB) <= Range))
                return (true);
        }
        else
            if (Distance(PosA, PosB) <= Range)
                return (true);
    }
    return (false);
}


int InRangeCount(int playerId = -1, int CollectorUnitID = -1, int TargetPlayerId = -1, int ClassTarget = -1, float Range = 0.0, bool isSquire = False)
{
    int CollectorIDs = xsGetPlayerUnitIds(playerId, CollectorUnitID);
    int UnitIDs = xsGetPlayerUnitIds(TargetPlayerId, ClassTarget);
    int ans = 0;
    int i = 0;
    for (i = 0; < xsArrayGetSize(UnitIDs))
        if (isInRange(xsArrayGetInt(UnitIDs, i), CollectorIDs, Range, isSquire))
            ans = ans + 1;
    return (ans);
}


bool AllyCiv(int playerId = -1, int civ = -1)
{
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if (i != playerId)
            if (isAlly(i, playerId) && (xsGetPlayerCivilization(i) == civ))
                return (true);
    return (false);
}


void SetInfinityStacking(int playerId = -1, int TechID = -1)
{
    xsEffectAmount(cModifyTech, TechID, cAttrSetStacking, 1, playerId);
}


void SetTechEffectID(int playerId = -1, int TechID = -1, int EffectID = -1)
{
    xsEffectAmount(cModifyTech, TechID, cAttrSetEffect, EffectID, playerId);
}


void ArrayMultipleSetInt(int ArrayID = -1, int StartIndex = -1, int num1 = -1, int num2 = -1, int num3 = -1, int num4 = -1, int num5 = -1, int num6 = -1, int num7 = -1, int num8 = -1, int num9 = -1, int num10 = -1)
{
    xsArraySetInt(ArrayID, StartIndex, num1);
    xsArraySetInt(ArrayID, StartIndex + 1, num2);
    xsArraySetInt(ArrayID, StartIndex + 2, num3);
    xsArraySetInt(ArrayID, StartIndex + 3, num4);
    xsArraySetInt(ArrayID, StartIndex + 4, num5);
    xsArraySetInt(ArrayID, StartIndex + 5, num6);
    xsArraySetInt(ArrayID, StartIndex + 6, num7);
    xsArraySetInt(ArrayID, StartIndex + 7, num8);
    xsArraySetInt(ArrayID, StartIndex + 8, num9);
    xsArraySetInt(ArrayID, StartIndex + 9, num10);
}


void AddAttackForm(int playerId = -1, int ClassTarget = -1, int DamageClass = -1, int DefaultValue = 0)
{
    xsEffectAmount(cSetAttribute, ClassTarget, cAddAttackType, DamageClass, playerId);
    if (DefaultValue != 0)
        ModAttack(playerId, ClassTarget, DamageClass, DefaultValue);
}


void AddArmorForm(int playerId = -1, int ClassTarget = -1, int DamageClass = -1, int DefaultValue = 0)
{
    xsEffectAmount(cSetAttribute, ClassTarget, cAddArmorType, DamageClass, playerId);
    if (DefaultValue != 0)
        ModArmor(playerId, ClassTarget, DamageClass, DefaultValue);
}


void PrintObjectTasks(int playerId = -1, int ObjectID = -1)
{
    int i = 0;
    int TaskCount = xsGetObjectTaskCount(ObjectID, playerId);
    PrintMessage("player = " + playerId + ", ObjectID = " + ObjectID);
    for (i = 0; < TaskCount)
    {
        xsObjectTaskAmount(ObjectID, playerId, i);
        PrintMessage("TaskType: " + xsGetTaskAmount(cTaskAttrTaskType) + ", ObjectID = " +
                     xsGetTaskAmount(cTaskAttrObjectId) + ", ObjectClass = " +
                     xsGetTaskAmount(cTaskAttrObjectClass));
    }
}


void ApplyModifyAllTargets(int playerId = -1, int ClassTarget = -1, bool includeBuildings = false, bool includeSiege = true, bool includeAnimals = false)
{
    xsTaskAmount(cTaskAttrObjectClass, cArcherClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cTradeBoatClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cVillagerClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cInfantryClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cCavalryClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cMonkClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cTradeCartClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cTransportShipClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cFishingBoatClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cWarshipClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cConquistadorClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cPhalanxClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cPetardClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cCavalryArcherClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cMonkWithRelicClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cHandCannoneerClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cScoutCavalryClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cKingClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    
    if (includeBuildings)
    {
        xsTaskAmount(cTaskAttrObjectClass, cBuildingClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cWallClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cGateClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cFarmClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cTowerClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    }
    if (includeSiege)
    {
        xsTaskAmount(cTaskAttrObjectClass, cSiegeWeaponClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cPackedUnitClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cUnpackedSiegeUnitClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cScorpionClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    }
    if (includeAnimals)
    {
        xsTaskAmount(cTaskAttrObjectClass, cPreyAnimalClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cPredatorAnimalClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cDomesticAnimalClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cLivestockClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cControlledAnimalClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    }
}


void ApplyModifyMilitaryTargets(int playerId = -1, int ClassTarget = -1, bool includeSiege = true)
{
    xsTaskAmount(cTaskAttrObjectClass, cArcherClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cInfantryClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cCavalryClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    
    xsTaskAmount(cTaskAttrObjectClass, cMonkClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cTransportShipClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cWarshipClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cConquistadorClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cPhalanxClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cPetardClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cCavalryArcherClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cMonkWithRelicClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cHandCannoneerClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cScoutCavalryClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);

    if (includeSiege)
    {
        xsTaskAmount(cTaskAttrObjectClass, cSiegeWeaponClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cPackedUnitClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cUnpackedSiegeUnitClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cScorpionClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    }
}


void ApplyModifyBuildingTargets(int playerId = -1, int ClassTarget = -1, bool includeWallsAndGates = true)
{
    xsTaskAmount(cTaskAttrObjectClass, cBuildingClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cFarmClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    xsTaskAmount(cTaskAttrObjectClass, cTowerClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    if (includeWallsAndGates)
    {
        xsTaskAmount(cTaskAttrObjectClass, cWallClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
        xsTaskAmount(cTaskAttrObjectClass, cGateClass);   xsModifyObjectTasks(ClassTarget, playerId, 1001);
    }
}


int KeyToHotkeyID(int KeyID = -1)
{
    int keyid = KeyID;
    if (keyid > 15)
        keyid = keyid - 20;
    switch (keyid)
    {
        case 1:
            return (QHotkeyID);
        case 2:
            return (WHotkeyID);
        case 3:
            return (EHotkeyID);
        case 4:
            return (RHotkeyID);
        case 5:
            return (THotkeyID);
        case 6:
            return (AHotkeyID);
        case 7:
            return (SHotkeyID);
        case 8:
            return (DHotkeyID);
        case 9:
            return (FHotkeyID);
        case 10:
            return (GHotkeyID);
        case 11:
            return (ZHotkeyID);
        case 12:
            return (XHotkeyID);
        case 13:
            return (CHotkeyID);
        case 14:
            return (VHotkeyID);
        default:
            return (-1);
    }
    return (-1);
}


int FindTask(int playerId = -1, int ObjectID = -1, int TaskType = -1, int TaskObjectClass = 899, int TaskObjectID = -1, float SearchWaitTime = -101.0)
{
    int TaskCount = xsGetObjectTaskCount(ObjectID, playerId);
    int i = 0;
    for (i = 0; < TaskCount)
    {
        xsObjectTaskAmount(ObjectID, playerId, i);
        if (xsGetTaskAmount(cTaskAttrTaskType) == TaskType)
        {
            if ((TaskObjectID != xsGetTaskAmount(cTaskAttrObjectId)) || (TaskObjectClass != xsGetTaskAmount(cTaskAttrObjectClass)))
                continue;
            if ((SearchWaitTime != -101.0) && (SearchWaitTime != xsGetTaskAmount(cTaskAttrSearchWaitTime)))
                continue;
            return (i);
        }
    }
    return (-1);
}


void AllySpawnUnit(int playerId = -1, int SpawnUnitID = -1, int SpawnBuidingID = -1, int SpawnNum = -1, int SpawnBuildingCap = 0, bool isInside = false)
{
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if ((i == playerId) || (isAlly(playerId, i)))
            SpawnUnit(i, SpawnUnitID, SpawnBuidingID, SpawnNum, SpawnBuildingCap, isInside);
}


bool isChroniclesCiv(int civ = -1)
{
    return ((civ == cAchaemenids) || (civ == cAthenians) || (civ == cSpartans) || (civ == cMacedonians) || (civ == cThracians) || (civ == cPuru));
}


void AddTrainLocation(int playerId = -1, int ClassTarget = -1, bool ResetIndex = true, int TrainLocationID = NullInt, int TrainTime = NullInt, int TrainButtonID = NullInt, int HotkeyID = NullInt)
{
    xsEffectAmount(cMulAttribute, ClassTarget, cTrainLocationsEntryMod, 32767, playerId);
    if (TrainLocationID != NullInt)
        xsEffectAmount(cSetAttribute, ClassTarget, cTrainLocation, TrainLocationID, playerId);
    if (TrainTime != NullInt)
        xsEffectAmount(cSetAttribute, ClassTarget, cTrainTime, TrainTime, playerId);
    if (TrainButtonID != NullInt)
        xsEffectAmount(cSetAttribute, ClassTarget, cTrainButton, TrainButtonID, playerId);
    if (HotkeyID != NullInt)
        xsEffectAmount(cSetAttribute, ClassTarget, cHotkeyId, HotkeyID, playerId);
    if (ResetIndex)
        xsEffectAmount(cSetAttribute, ClassTarget, cTrainLocationsEntryMod, 0, playerId);
}


int FindTrainLocation(int playerId = -1, int ObjectID = -1, int TrainLocationID = -1, bool ResetIndex = false)
{
    int i = 0;
    int TotalNum = xsGetObjectAttribute(playerId, ObjectID, cTrainLocationsTotalNum);
    int TrainLocation = 0;
    if (TotalNum == 0)
        return (-1);
    for (i = 0; < TotalNum)
    {
        xsEffectAmount(cSetAttribute, ObjectID, cTrainLocationsEntryMod, i, playerId);
        TrainLocation = xsGetObjectAttribute(playerId, ObjectID, cTrainLocation);
        if (TrainLocation == TrainLocationID)
        {
            if (ResetIndex)
                xsEffectAmount(cSetAttribute, ObjectID, cTrainLocationsEntryMod, 0);
            return (i);
        }
    }
    xsEffectAmount(cSetAttribute, ObjectID, cTrainLocationsEntryMod, 0, playerId);
    return (-1);
}


void SetTrainLocationAttr(int playerId = -1, int ObjectID = -1, int TrainLocationID = -1, int TargetAttr = -1, float value = -1.0, bool ResetIndex = true)
{
    int TrainLocationIndex = FindTrainLocation(playerId, ObjectID, TrainLocationID);
    if (TrainLocationIndex == -1)
        return;
    xsEffectAmount(cSetAttribute, ObjectID, TargetAttr, value, playerId);
    if (ResetIndex)
        xsEffectAmount(cSetAttribute, ObjectID, cTrainLocationsEntryMod, 0);
}


void ModTrainLocationAttr(int playerId = -1, int ObjectID = -1, int TrainLocationID = -1, int TargetAttr = -1, float value = -1.0, bool ResetIndex = true)
{
    int TrainLocationIndex = FindTrainLocation(playerId, ObjectID, TrainLocationID);
    if (TrainLocationIndex == -1)
        return;
    xsEffectAmount(cAddAttribute, ObjectID, TargetAttr, value, playerId);
    if (ResetIndex)
        xsEffectAmount(cSetAttribute, ObjectID, cTrainLocationsEntryMod, 0);
}


void MulTrainLocationAttr(int playerId = -1, int ObjectID = -1, int TrainLocationID = -1, int TargetAttr = -1, float value = -1.0, bool ResetIndex = true)
{
    int TrainLocationIndex = FindTrainLocation(playerId, ObjectID, TrainLocationID);
    if (TrainLocationIndex == -1)
        return;
    xsEffectAmount(cMulAttribute, ObjectID, TargetAttr, value, playerId);
    if (ResetIndex)
        xsEffectAmount(cSetAttribute, ObjectID, cTrainLocationsEntryMod, 0);
}


void PrintTrainLocations(int playerId = -1, int ObjectID = -1)
{
    int i = 0;
    int TotalNum = xsGetObjectAttribute(playerId, ObjectID, cTrainLocationsTotalNum);
    for (i = 0; < TotalNum)
    {
        SetAttribute(playerId, ObjectID, cTrainLocationsEntryMod, i);
        PrintMessage("ID = " + ObjectID + ", TLID = " + xsGetObjectAttribute(playerId, ObjectID, cTrainLocation) + ", t = " + xsGetObjectAttribute(playerId, ObjectID, cTrainTime)
            + ", BTN = " + xsGetObjectAttribute(playerId, ObjectID, cTrainButton) + ", HK = " + xsGetObjectAttribute(playerId, ObjectID, cHotkeyId));
    }
    SetAttribute(playerId, ObjectID, cTrainLocationsEntryMod, 0);
}


bool MinAge(int playerId = -1, int AgeID = -1)
{
    int Age = xsPlayerAttribute(playerId, cAttributeCurrentAge);
    return (Age >= AgeID);
}


bool isAge(int playerId = -1, int AgeID = -1)
{
    int Age = xsPlayerAttribute(playerId, cAttributeCurrentAge);
    return (Age == AgeID);
}


bool isEzsCiv(int CivID = -1)
{
    return ((CivID == cJurchens));
}


bool isPopLeft(int playerId = -1)
{
    return (xsPlayerAttribute(playerId, cAttributePopulationCap) > 0);
}