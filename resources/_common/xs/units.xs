//  Functions related to units


bool isHouse(int ObjectID = -1)
{
    return ((ObjectID == 70) || (ObjectID == 463) || (ObjectID == 464) || (ObjectID == 465) || (ObjectID == 191) || (ObjectID == 192));
}


bool isCastle(int ObjectID = -1)
{
    return (ObjectID == 82);
}


bool isBarrack(int ObjectID = -1)
{
    return ((ObjectID == 12) || (ObjectID == 20) || (ObjectID == 132) || (ObjectID == 498));
}


bool isArcherRange(int ObjectID = -1)
{
    return ((ObjectID == 10) || (ObjectID == 14) || (ObjectID == 87));
}


bool isStable(int ObjectID = -1)
{
    return ((ObjectID == 86) || (ObjectID == 101) || (ObjectID == 153));
}


bool isBlackSmith(int ObjectID = -1)
{
    return ((ObjectID == 18) || (ObjectID == 19) || (ObjectID == 103) || (ObjectID == 105));
}


bool isMarket(int ObjectID = -1)
{
    return ((ObjectID == 84) || (ObjectID == 116) || (ObjectID == 137) || (ObjectID == 1646));
}


bool isSiegeWorkshop(int ObjectID = -1)
{
    return ((ObjectID == 49) || (ObjectID == 150));
}


bool isUniversity(int ObjectID = -1)
{
    return ((ObjectID == 209) || (ObjectID == 210));
}


bool isMonastery(int ObjectID = -1)
{
    return ((ObjectID == 30) || (ObjectID == 31) || (ObjectID == 32) || (ObjectID == 104));
}


bool isWonder(int ObjectID = -1)
{
    return (ObjectID == 276);
}


bool isTownCenter(int ObjectID = -1)
{
    return ((ObjectID == 71) || (ObjectID == 109) || (ObjectID == 141) || (ObjectID == 142));
}


bool isDock(int ObjectID = -1)
{
    return ((ObjectID == 45) || (ObjectID == 47) || (ObjectID == 51) || (ObjectID == 133) || (ObjectID == 1189));
}


bool isLandMilitaryClass(int ClassID = -1)
{
    return ((ClassID == cArcherClass) || (ClassID == cInfantryClass) || (ClassID == cCavalryClass) || (ClassID == cSiegeWeaponClass) || (ClassID == cMonkClass)
            || (ClassID == cConquistadorClass) || (ClassID == cPetardClass) || (ClassID == cCavalryArcherClass) || (ClassID == cMonkWithRelicClass)
            || (ClassID == cHandCannoneerClass) || (ClassID == cScoutCavalryClass) || (ClassID == cPackedUnitClass) || (ClassID == cUnpackedSiegeUnitClass)
            || (ClassID == cScorpionClass));
}


bool isLandMilitaryObject(int ObjectID = -1)
{
    return (isLandMilitaryClass(xsGetObjectClass(ObjectID)));
}


bool isLandMilitaryUnit(int UnitID = -1)
{
    return (isLandMilitaryClass(xsGetUnitClass(UnitID)));
}


bool isMilitaryClass(int ClassID = -1)
{
    return ((ClassID == cArcherClass) || (ClassID == cInfantryClass) || (ClassID == cCavalryClass) || (ClassID == cSiegeWeaponClass) || (ClassID == cMonkClass) || (ClassID == cTransportShipClass) || (ClassID == cWarshipClass)
            || (ClassID == cConquistadorClass) || (ClassID == cPetardClass) || (ClassID == cCavalryArcherClass) || (ClassID == cMonkWithRelicClass) || (ClassID == cHandCannoneerClass) || (ClassID == cScoutCavalryClass) || (ClassID == cPackedUnitClass) || (ClassID == cUnpackedSiegeUnitClass)
            || (ClassID == cScorpionClass));
}


bool isMilitaryObject(int ObjectID = -1)
{
    return (isMilitaryClass(xsGetObjectClass(ObjectID)));
}


bool isMilitaryUnit(int UnitID = -1)
{
    return (isMilitaryClass(xsGetUnitClass(UnitID)));
}


bool isEconomicClass(int ClassID = -1)
{
    return ((ClassID == cTradeBoatClass) || (ClassID == cVillagerClass) || (ClassID == cTradeCartClass) || (ClassID == cFishingBoatClass));
}


bool isEconomicObject(int ObjectID = -1)
{
    return (isEconomicClass(xsGetObjectClass(ObjectID)));
}


bool isEconomicUnit(int UnitID = -1)
{
    return (isEconomicClass(xsGetUnitClass(UnitID)));
}


bool isBuildingClass(int ClassID = -1)
{
    return ((ClassID == cBuildingClass) || (ClassID == cWallClass) || (ClassID == cGateClass) || (ClassID == cTowerClass) || (ClassID == cFarmClass));
}


bool isBuildingObject(int ObjectID = -1)
{
    return (isBuildingClass(xsGetObjectClass(ObjectID)));
}


bool isBuildingUnit(int UnitID = -1)
{
    return (isBuildingClass(xsGetUnitClass(UnitID)));
}


bool isAnimalClass(int ClassID = -1)
{
    return ((ClassID == cPreyAnimalClass) || (ClassID == cPredatorAnimalClass) || (ClassID == cDomesticAnimalClass)
            || (ClassID == cLivestockClass) || (ClassID == cControlledAnimalClass));
}


bool isAnimalObject(int ObjectID = -1)
{
    return (isAnimalClass(xsGetObjectClass(ObjectID)));
}


bool isAnimalUnit(int UnitID = -1)
{
    return (isAnimalClass(xsGetUnitClass(UnitID)));
}


bool isResourceClass(int ClassID = -1)
{
    return ((ClassID == cSeaFishClass) || (ClassID == cForageBushClass) || (ClassID == cStoneMineClass) || (ClassID == cPreyAnimalClass)
            || (ClassID == cPredatorAnimalClass) || (ClassID == cTreeClass) || (ClassID == cTreeStumpClass) || (ClassID == cGoldMine)
            || (ClassID == cShoreFish) || (ClassID == cResourcePileClass) || (ClassID == cOreMineClass) || (ClassID == cGoldFishClass));
}


bool isClassOperable(int ClassID = -1)
{
    return(isMilitaryClass(ClassID) || isEconomicClass(ClassID) || isBuildingClass(ClassID) || (ClassID == cKingClass));
}


bool isObjectOperable(int ObjectID = -1)
{
    return (isClassOperable(xsGetObjectClass(ObjectID)));
}


bool isUnitOperable(int UnitID = -1)
{
    return (isClassOperable(xsGetUnitClass(UnitID)));
}


bool isGarrison(int UnitID1 = -1, int UnitID2 = -1)
{
    return (xsGetUnitPosition(UnitID1) == xsGetUnitPosition(UnitID2));
}


//  Consume a relic
//  Relics always belong to Gaia even captured by players
bool ConsumeRelic(int playerId = -1)
{
    static int RelicList = 0;
    if (RelicList == 0)
        RelicList = xsGetPlayerUnitIds(0, cRelicClass);
    else
        RelicList = xsGetPlayerUnitIds(0, cRelicClass, RelicList);
    int i = 0;
    for (i = 0; < xsArrayGetSize(RelicList))
    {
        int RelicUnitID = xsArrayGetInt(RelicList, i);
        int UnitID = xsGetGarrisonedInUnitId(RelicUnitID);
        if (xsGetUnitOwner(UnitID) == playerId)
        {
            xsRemoveUnit(RelicUnitID);
            return (true);
        }
    }
    return (false);
}


int UniqueUnitTechIDArray = -1;
int EliteUniqueUnitTechIDArray = -1;


void UniqueUnitInit()
{
        UniqueUnitTechIDArray = xsArrayCreateInt(100, 0);
        ArrayMultipleSetInt(UniqueUnitTechIDArray, 1, 263, 275, 446, 276, 262, 268, 267, 274, 269, 271);
        ArrayMultipleSetInt(UniqueUnitTechIDArray, 11, 399, 273, 277, 58, 431, 26, 1, 449, 467, 839);
        ArrayMultipleSetInt(UniqueUnitTechIDArray, 21, 508, 471, 503, 562, 568, 566, 564, 614, 616, 618);
        ArrayMultipleSetInt(UniqueUnitTechIDArray, 31, 620, 677, 679, 681, 683, 750, 752, 778, 780, 825);
        ArrayMultipleSetInt(UniqueUnitTechIDArray, 41, 827, 829, 881, 917, 919, 1114, 1124, 1134, 1063, 1073);
        ArrayMultipleSetInt(UniqueUnitTechIDArray, 51, 1035, 990, 1001, 1288, 1300, 1325, 1363, 1375, 1388, 0);

        EliteUniqueUnitTechIDArray = xsArrayCreateInt(100, 0);
        ArrayMultipleSetInt(EliteUniqueUnitTechIDArray, 1, 360, 363, 365, 364, 366, 362, 361, 367, 368, 369);
        ArrayMultipleSetInt(EliteUniqueUnitTechIDArray, 11, 398, 371, 370, 60, 432, 27, 2, 450, 468, 840);
        ArrayMultipleSetInt(EliteUniqueUnitTechIDArray, 21, 509, 472, 504, 563, 569, 567, 565, 615, 617, 619);
        ArrayMultipleSetInt(EliteUniqueUnitTechIDArray, 31, 621, 678, 680, 682, 684, 751, 753, 779, 781, 826);
        ArrayMultipleSetInt(EliteUniqueUnitTechIDArray, 41, 828, 830, 882, 918, 920, 1115, 1125, 1135, 1064, 1074);
        ArrayMultipleSetInt(EliteUniqueUnitTechIDArray, 51, 1036, 991, 1002, 1289, 1301, 1326, 1364, 1376, 1389, 0);
}


int GetUniqueUnitID(int CivID = -1, bool isElite = false)
{
    static int UniqueUnitIDArray = -1;
    static int EliteUniqueUnitIDArray = -1;
    if (UniqueUnitIDArray == -1)
    {
        UniqueUnitIDArray = xsArrayCreateInt(100, 0);
        ArrayMultipleSetInt(UniqueUnitIDArray, 1, 8, 281, 41, 25, 291, 73, 40, 239, 282, 46);
        ArrayMultipleSetInt(UniqueUnitIDArray, 11, 692, 11, 232, 771, 725, 763, 755, 827, 866, 1747);
        ArrayMultipleSetInt(UniqueUnitIDArray, 21, 879, 869, 876, 1001, 1016, 1013, 1007, 1120, 1123, 1126);
        ArrayMultipleSetInt(UniqueUnitIDArray, 31, 1129, 1225, 1228, 1231, 1234, 1655, 1658, 1701, 1704, 1735);
        ArrayMultipleSetInt(UniqueUnitIDArray, 41, 1759, 1741, 1790, 1800, 1803, 2101, 2104, 2107, 1959, 1968);
        ArrayMultipleSetInt(UniqueUnitIDArray, 51, 1949, 1908, 1920, 2382, 2386, 2388, 2562, 2566, 2579, 0);

        EliteUniqueUnitIDArray = xsArrayCreateInt(100, 0);
        ArrayMultipleSetInt(EliteUniqueUnitIDArray, 1, 530, 531, 555, 554, 560, 559, 553, 558, 556, 557);
        ArrayMultipleSetInt(EliteUniqueUnitIDArray, 11, 694, 561, 534, 773, 726, 765, 757, 829, 868, 1749);
        ArrayMultipleSetInt(EliteUniqueUnitIDArray, 21, 881, 871, 878, 1003, 1018, 1015, 1009, 1122, 1125, 1128);
        ArrayMultipleSetInt(EliteUniqueUnitIDArray, 31, 1131, 1227, 1230, 1233, 1236, 1657, 1659, 1703, 1706, 1737);
        ArrayMultipleSetInt(EliteUniqueUnitIDArray, 41, 1761, 1743, 1792, 1802, 1805, 2102, 2105, 2108, 1961, 1970);
        ArrayMultipleSetInt(EliteUniqueUnitIDArray, 51, 1951, 1910, 1922, 2383, 2387, 2389, 2564, 2568, 2581, 0);
    }
    if (isElite)
        return (xsArrayGetInt(EliteUniqueUnitIDArray, CivID));
    return (xsArrayGetInt(UniqueUnitIDArray, CivID));
}