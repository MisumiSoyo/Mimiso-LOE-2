//======================================================================================
//
// This file contains functions which are called by technology effects.
// Included automatically.
//
//======================================================================================

//======================================================================================
// Object IDs
//======================================================================================

const int VillagerMaleID = 83;
const int VillagerFemaleID = 293;
const int BuilderMaleID = 118;
const int BuilderFemaleID = 212;
const int RepairerMaleID = 156;
const int RepairerFemaleID = 222;
const int FarmerMaleID = 214;
const int FarmerFemaleID = 259;
const int GoldMinerMaleID = 579;
const int GoldMinerFemaleID = 581;
const int ForagerMaleID = 120;
const int ForagerFemaleID = 354;
const int StoneMinerMaleID = 124;
const int StoneMinerFemaleID = 220;
const int LumberjackMaleID = 123;
const int LumberjackFemaleID = 218;
const int HunterMaleID = 122;
const int HunterFemaleID = 216;
const int FishermanMaleID = 56;
const int FishermanFemaleID = 57;
const int ShepherdMaleID = 590;
const int ShepherdFemaleID = 592;
const int HerderMaleID = 1891;
const int HerderFemaleID = 1892;
const int OystererMaleID = 2333;
const int OystererFemaleID = 2334;

const int EliteSkirmisherID = 6;
const int SkirmisherID = 7;
const int FishingShipID = 13;
const int Monastery2ID = 30;
const int Monastery3ID = 31;
const int Monastery4ID = 32;
const int TownCenterProjID = 54;
const int TownCenterFnd2ID = 71;
const int MilitiaID = 74;
const int ManAtArmsID = 75;
const int LongSwordsmanID = 77;
const int CastleID = 82;
const int SpearmanID = 93;
const int Monastery1ID = 104;
const int TownCenterFnd1ID = 109;
const int TownCenterFnd3ID = 141;
const int TownCenterFnd4ID = 142;
const int SlingerID = 185;
const int MamelukeID = 282;
const int Llama1ID = 305;
const int TownCenterFireProjID = 328;
const int PikemanID = 358;
const int HalberdierID = 359;
const int TowerProjID = 505;
const int TowerFireProjID = 518;
const int DemoShipID = 527;
const int HeavyDemoShipID = 528;
const int EliteMamelukeID = 556;
const int ChampionID = 567;
const int CastleProjID = 746;
const int CastleFireProjID = 747;
const int EliteTarkanID = 757;
const int KrepostProjID = 786;
const int KrepostFireProjID = 787;
const int DemoRaftID = 1104;
const int BallistaElephantID = 1120;
const int EliteBallistaElephantID = 1122;
const int ImperialSkirmisherID = 1155;
const int EliteKipchakID = 1233;
const int SaladinID = 1296;
const int JarlID = 1298;
const int ProjectileChurchID = 1548;
const int EliteSerjeantID = 1661;
const int FlemishMilitiaID = 1699;
const int SpearmanDonjonID = 1786;
const int PikemanDonjonID = 1787;
const int HalberdierDonjonID = 1788;
const int FortifiedChurchID = 1806;
const int WarriorPriestWithRelicID = 1831;
const int HunnicHorseID = 1869;
const int MountedTrebuchetID = 1923;
const int CaoCaoID = 1954;
const int WhiteFeatherGuardID = 1959;
const int EliteWhiteFeatherGuardID = 1961;
const int WarChariotFocusID = 1962;
const int Llama2ID = 1963;
const int LiuBeiID = 1966;
const int FireArcherID = 1968;
const int EliteFireArcherID = 1970;
const int SunJianID = 1978;
const int WarChariotBarrageID = 1980;
const int ZhouYuID = 2044;
const int LiuBiaoID = 2049;
const int Settlement1ID = 2556;
const int Settlement2ID = 2558;
const int Settlement3ID = 2560;
const int GuechaWarriorID = 2562;
const int EliteGuechaWarriorID = 2564;
const int EliteKonaID = 2568;
const int BlackWoodArcherID = 2579;
const int EliteBlackWoodArcherID = 2581;
const int ProjectileDockID = 2631;
const int ProjectileDockFireID = 2632;
const int VarangianGuardID = 2703;
const int EliteVarangianGuardID = 2704;

const int MonoremeID = 2127;
const int BiremeID = 2128;
const int TriremeID = 2129;
const int HopliteID = 2110;
const int EliteHopliteID = 2111;
const int RhomphaiaWarriorID = 2386;
const int EliteRhomphaiaWarriorID = 2387;

//======================================================================================
// Effects Functions
//======================================================================================

// 1 - Inca team bonus: spawn a randomized llama
void EffectFunction1(int playerId = -1)
{
    int targetLlama = Llama1ID;
    int randomNumber = xsGetRandomNumberLH(0, 2);
    if (randomNumber == 1)
    {
        targetLlama = Llama2ID;
    }
    xsEffectAmount(cSpawnUnit, targetLlama, 619, 1, playerId);
}

// Handicap effects
void HandicapSetup(int playerId = -1)
{
  float handicapMultiplier = xsGetHandicapMultiplier(playerId);
  if (handicapMultiplier <= 1)
  {
      return;
  }
  float trainTimeMultiplier = 1.0 / handicapMultiplier;

  xsEffectAmount(cMulAttribute, cBuildingClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cWallClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cGateClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cTowerClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cFarmClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cFarmClass, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cTradeCartClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cTradeCartClass, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cTradeBoatClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cTradeBoatClass, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cFishingBoatClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cFishingBoatClass, cCarryCapacity, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cVillagerClass, cHitpoints, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cVillagerClass, cCarryCapacity, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, VillagerMaleID, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, VillagerFemaleID, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, BuilderMaleID, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, BuilderFemaleID, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, RepairerMaleID, cWorkRate, handicapMultiplier, playerId);
  xsEffectAmount(cMulAttribute, RepairerFemaleID, cWorkRate, handicapMultiplier, playerId);

  xsEffectAmount(cMulResource, cAttributeFoodBonus, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeWoodBonus, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeGoldBonus, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeStoneBonus, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeFishingProductivity, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeShepherdingProductivity, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeHuntingProductivity, -1, handicapMultiplier, playerId);
  xsEffectAmount(cMulResource, cAttributeForagingProductivity, -1, handicapMultiplier, playerId);

  xsEffectAmount(cMulAttribute, cArcherClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cInfantryClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cCavalryClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cSiegeWeaponClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cMonkClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cWarshipClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cConquistadorClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cWarElephantClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cElephantArcherClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cPhalanxClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cPetardClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cCavalryArcherClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cMonkWithRelicClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cHandCannoneerClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cTwoHandedSwordsmanClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cPikemanClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cScoutCavalryClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cSpearmanClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cPackedUnitClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cUnpackedSiegeUnitClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cScorpionClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cRaiderClass, cTrainTime, trainTimeMultiplier, playerId);
  xsEffectAmount(cMulAttribute, cCavalryRaiderClass, cTrainTime, trainTimeMultiplier, playerId);
}

// Randomize graphics for Hunnic Horse
void HunnicHorseGraphic(int playerId = -1)
{
    int newAttackGraphicId = -1;
    int newStandingGraphicId = -1;
    int newDyingGraphicId = -1;
    int newUndeadGraphicId = -1;
    int newWalkingGraphicId = -1;

    int randomNumber = xsGetRandomNumberLH(0, 4);
    switch (randomNumber)
    {
        case 1:
        {
            newAttackGraphicId = 5600;
            newStandingGraphicId = 5602;
            newDyingGraphicId = 5601;
            newUndeadGraphicId = 5604;
            newWalkingGraphicId = 5605;
            break;
        }
        case 2:
        {
            newAttackGraphicId = 5606;
            newStandingGraphicId = 5608;
            newDyingGraphicId = 5607;
            newUndeadGraphicId = 5610;
            newWalkingGraphicId = 5611;
            break;
        }
        case 3:
        {
            newAttackGraphicId = 5612;
            newStandingGraphicId = 5614;
            newDyingGraphicId = 5613;
            newUndeadGraphicId = 5616;
            newWalkingGraphicId = 5617;
            break;
        }
        default:
        {
            return;
        }
    }

    xsEffectAmount(cSetAttribute, HunnicHorseID, cAttackGraphic, newAttackGraphicId, playerId);
    xsEffectAmount(cSetAttribute, HunnicHorseID, cStandingGraphic, newStandingGraphicId, playerId);
    xsEffectAmount(cSetAttribute, HunnicHorseID, cDyingGraphic, newDyingGraphicId, playerId);
    xsEffectAmount(cSetAttribute, HunnicHorseID, cUndeadGraphic, newUndeadGraphicId, playerId);
    xsEffectAmount(cSetAttribute, HunnicHorseID, cWalkingGraphic, newWalkingGraphicId, playerId);
}

// 2 - Dark Age effect
void EffectFunction2(int playerId = -1)
{
    HandicapSetup(playerId);
    HunnicHorseGraphic(playerId);
}

// Remove Ordo Cavalry from undesirable units
void OrdoCavalryRemoval(int UnitTarget = -1, int playerId = -1)
{
  xsEffectAmount(cAddAttribute, UnitTarget, cCombatAbility, -128, playerId);
  xsModifyObjectTasks(UnitTarget, playerId, -1);

}

// 3 - Apply Ordo Cavalry to Cavalry Classes
void EffectFunction3(int playerId = -1)
{
  int TargetClass = 0;
  xsResetTaskAmount();
  
  xsTaskAmount(cTaskAttrWorkValue1, 1.5);
  xsTaskAmount(cTaskAttrWorkValue2, 2);
  xsTaskAmount(cTaskAttrSearchWaitTime, 120);

  TargetClass = cFlagClassRemoval * (cFlagClassOffset + cFlagClassBuilding);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass); // All except Buildings
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeStinger);

  xsEffectAmount(cAddAttribute, cCavalryClass, cCombatAbility, 128, playerId);
  xsModifyObjectTasks(cCavalryClass, playerId, 0);

  xsEffectAmount(cAddAttribute, cScoutCavalryClass, cCombatAbility, 128, playerId);
  xsModifyObjectTasks(cScoutCavalryClass, playerId, 0);

  OrdoCavalryRemoval(MountedTrebuchetID, playerId);
  OrdoCavalryRemoval(MamelukeID, playerId);
  OrdoCavalryRemoval(EliteMamelukeID, playerId);
  OrdoCavalryRemoval(SaladinID, playerId);
  OrdoCavalryRemoval(JarlID, playerId);
  OrdoCavalryRemoval(LiuBiaoID, playerId);
  OrdoCavalryRemoval(BallistaElephantID, playerId);
  OrdoCavalryRemoval(EliteBallistaElephantID, playerId);
  OrdoCavalryRemoval(WarChariotFocusID, playerId);
  OrdoCavalryRemoval(WarChariotBarrageID, playerId);

  xsResetTaskAmount();
}

// 4 - Effect of Tuntian for Wei
void EffectFunction4(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeMilitaryFoodTrickle);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 3);
  xsTaskAmount(cTaskAttrSearchWaitTime, 1);
  xsTaskAmount(cTaskAttrAutoSearch, 3);
  xsTaskAmount(cTaskAttrEnableTargeting, 1);
  xsTaskAmount(cTaskAttrOwnerType, 5);
  xsTaskAmount(cTaskAttrGatherType, 1);

  xsTask(cArcherClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cInfantryClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cCavalryClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cConquistadorClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cPetardClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cCavalryArcherClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cHandCannoneerClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(cScoutCavalryClass, cTaskTypeGenerateResources, -1, playerId);
  xsTask(WarriorPriestWithRelicID, cTaskTypeGenerateResources, -1, playerId);

  xsResetTaskAmount();
}

// 5 - Effect of Chieftains for Vikings
void EffectFunction5(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 20);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeInfantryKillReward);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  xsTask(cInfantryClass, cTaskTypeLoot, cTradeBoatClass, playerId);
  xsTask(cInfantryClass, cTaskTypeLoot, cMonkWithRelicClass, playerId);
  xsTask(cInfantryClass, cTaskTypeLoot, cMonkClass, playerId);
  xsTask(cInfantryClass, cTaskTypeLoot, cMonkWithRelicClass, playerId);
  xsTask(cInfantryClass, cTaskTypeLoot, WarriorPriestWithRelicID, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 5);
  xsTask(cInfantryClass, cTaskTypeLoot, cVillagerClass, playerId);

  xsResetTaskAmount();
}

// Effect of Coiled Serpent Array for Shu
void CoiledSerpentArray(int UnitClass = -1, int playerId = -1)
{
  xsEffectAmount(cAddAttribute, UnitClass, cCombatAbility, 96, playerId);
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.15);
  xsTaskAmount(cTaskAttrWorkValue2, 30);
  xsTaskAmount(cTaskAttrWorkRange, 15);
  xsTaskAmount(cTaskAttrGatheringSoundInt32, 13406);
  xsTaskAmount(cTaskAttrDepositSoundInt32, 13406);
  xsTaskAmount(cTaskAttrOwnerType, 1);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 3);
  xsTaskAmount(cTaskAttrSearchWaitTime, 0);
  xsTaskAmount(cTaskAttrAutoSearch, 0);
  xsTask(UnitClass, cTaskTypeAura, SpearmanID, playerId);

  xsTaskAmount(cTaskAttrAutoSearch, 1);
  xsTask(UnitClass, cTaskTypeAura, PikemanID, playerId);
  xsTask(UnitClass, cTaskTypeAura, HalberdierID, playerId);
  xsTask(UnitClass, cTaskTypeAura, SpearmanDonjonID, playerId);
  xsTask(UnitClass, cTaskTypeAura, PikemanDonjonID, playerId);
  xsTask(UnitClass, cTaskTypeAura, HalberdierDonjonID, playerId);
  xsTask(UnitClass, cTaskTypeAura, WhiteFeatherGuardID, playerId);
  xsTask(UnitClass, cTaskTypeAura, EliteWhiteFeatherGuardID, playerId);

  xsResetTaskAmount();
}

// 6 - Apply Coiled Serpent Array to desired units for Shu
void EffectFunction6(int playerId = -1)
{
  xsResetTaskAmount();

  CoiledSerpentArray(SpearmanID, playerId);
  CoiledSerpentArray(PikemanID, playerId);
  CoiledSerpentArray(HalberdierID, playerId);
  CoiledSerpentArray(SpearmanDonjonID, playerId);
  CoiledSerpentArray(PikemanDonjonID, playerId);
  CoiledSerpentArray(HalberdierDonjonID, playerId);
  CoiledSerpentArray(WhiteFeatherGuardID, playerId);
  CoiledSerpentArray(EliteWhiteFeatherGuardID, playerId);

  xsResetTaskAmount();
}

// 7 - Effect of Bimaristan for Saracens
void EffectFunction7(int playerId = -1)
{
  int TargetClass = 0;

  xsResetTaskAmount();

  xsEffectAmount(cAddAttribute, cMonkClass, cCombatAbility, 32, playerId);
  xsEffectAmount(cAddAttribute, cMonkWithRelicClass, cCombatAbility, 32, playerId);
  xsEffectAmount(cAddAttribute, WarriorPriestWithRelicID, cCombatAbility, -32, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 75);
  xsTaskAmount(cTaskAttrWorkValue2, 1);
  xsTaskAmount(cTaskAttrWorkRange, 5);
  xsTaskAmount(cTaskAttrGatheringSoundInt32, 13404);
  xsTaskAmount(cTaskAttrDepositSoundInt32, 13404);
  xsTaskAmount(cTaskAttrOwnerType, 4);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 2);
  xsTaskAmount(cTaskAttrSearchWaitTime, 109);
  xsTaskAmount(cTaskAttrGatherType, 21);

  TargetClass = cFlagClassRemoval * (cFlagClassOffset + cFlagClassBuilding + cFlagClassSiege + cFlagClassShip);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass); // All except Buildings, Ships and Siege
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeAura);

  xsModifyObjectTasks(cMonkClass, playerId, 0);
  xsModifyObjectTasks(cMonkWithRelicClass, playerId, 0);
  xsModifyObjectTasks(WarriorPriestWithRelicID, playerId, -1);

  xsResetTaskAmount();
}

// 8 - Effect of Stronghold for Celts
void EffectFunction8(int playerId = -1)
{
  xsResetTaskAmount();

  xsEffectAmount(cAddAttribute, CastleID, cCombatAbility, 32, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 30);
  xsTaskAmount(cTaskAttrWorkValue2, 1);
  xsTaskAmount(cTaskAttrWorkRange, 7);
  xsTaskAmount(cTaskAttrGatheringSoundInt32, 13405);
  xsTaskAmount(cTaskAttrDepositSoundInt32, 13405);
  xsTaskAmount(cTaskAttrOwnerType, 4);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 4);
  xsTaskAmount(cTaskAttrSearchWaitTime, 109);
  xsTaskAmount(cTaskAttrGatherType, 21);
  xsTask(CastleID, cTaskTypeAura, cInfantryClass, playerId);
  xsTask(CastleID, cTaskTypeAura, WarriorPriestWithRelicID, playerId);

  xsResetTaskAmount();
}


// 9 - Effect of Fortified Church Bonus for Georgians
void ChurchAura(int BuildingID = -1, int playerId = -1)
{
  xsEffectAmount(cAddAttribute, BuildingID, cCombatAbility, 32, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 0.18);
  xsTask(BuildingID, cTaskTypeAura, FarmerMaleID, playerId);
  xsTask(BuildingID, cTaskTypeAura, FarmerFemaleID, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 0.1);
  xsTask(BuildingID, cTaskTypeAura, cVillagerClass, playerId);
  xsTask(BuildingID, cTaskTypeAura, cFarmClass, playerId);
}

// 9 - Apply Fortified Church Bonus for Georgians
void EffectFunction9(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue2, 1);
  xsTaskAmount(cTaskAttrWorkRange, 9);
  xsTaskAmount(cTaskAttrGatheringSoundInt32, 13402);
  xsTaskAmount(cTaskAttrDepositSoundInt32, 13402);
  xsTaskAmount(cTaskAttrOwnerType, 1);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 5);
  xsTaskAmount(cTaskAttrSearchWaitTime, 13);

  ChurchAura(Monastery1ID, playerId);
  ChurchAura(Monastery2ID, playerId);
  ChurchAura(Monastery3ID, playerId);
  ChurchAura(Monastery4ID, playerId);
  ChurchAura(FortifiedChurchID, playerId);

  xsResetTaskAmount();
}

// Apply Red Cliff Tactics for Wu
void RedCliffs(int UnitTarget = -1, int playerId = -1)
{
  int TargetClass =0;
  xsEffectAmount(cAddAttribute, UnitTarget, cCombatAbility, 128, playerId);

  xsTaskAmount(cTaskAttrProceedingGraphic, -1);
  TargetClass = (cFlagClassOffset + cFlagClassBuilding);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass);
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeStinger);

  xsModifyObjectTasks(UnitTarget, playerId, 0);
  xsTaskAmount(cTaskAttrProceedingGraphic, 13066);
  TargetClass = (cFlagClassOffset + cFlagClassShip);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass);

  xsModifyObjectTasks(UnitTarget, playerId, 0);
}

// 10 - Effect of Red Cliff Tactics for Wu
void EffectFunction10(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, -300);
  xsTaskAmount(cTaskAttrWorkValue2, 5);
  xsTaskAmount(cTaskAttrWorkRange, 5);
  xsTaskAmount(cTaskAttrSearchWaitTime, 109);

  RedCliffs(DemoShipID, playerId);
  RedCliffs(HeavyDemoShipID, playerId);
  RedCliffs(DemoRaftID, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, -60);

  RedCliffs(FireArcherID, playerId);
  RedCliffs(EliteFireArcherID, playerId);
  RedCliffs(ZhouYuID, playerId);

  xsResetTaskAmount();
}

// 11 - Effect of Gold Miner bonus for Malians
void EffectFunction11(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeExtraGoldProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

  xsTask(GoldMinerMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(GoldMinerFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(OystererMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(OystererFemaleID, cTaskTypeAdditionalResource, -1, playerId);

  xsResetTaskAmount();
}

// 12 - Effect of Forager bonus for Portuguese
void EffectFunction12(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeForagingWoodProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeWood);

  xsTask(ForagerMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ForagerFemaleID, cTaskTypeAdditionalResource, -1, playerId);

  xsResetTaskAmount();
}

// 13 - Effect of Stone Miner bonus for Poles
void EffectFunction13(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeStoneGoldMiningProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

  xsTask(StoneMinerMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(StoneMinerFemaleID, cTaskTypeAdditionalResource, -1, playerId);

  xsResetTaskAmount();
}

// 14 - Effect of Burgundian Vineyards for Burgundians
void EffectFunction14(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeGoldFarmingProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
  xsTaskAmount(cTaskAttrSearchWaitTime, 3);
  xsTaskAmount(cTaskAttrAutoSearch, 1);
  xsTaskAmount(cTaskAttrEnableTargeting, 1);
  xsTaskAmount(cTaskAttrOwnerType, 5);
  xsTaskAmount(cTaskAttrGatherType, 1);

  xsTask(FarmerMaleID, cTaskTypeGenerateResources, cFarmClass, playerId);
  xsTask(FarmerFemaleID, cTaskTypeGenerateResources, cFarmClass, playerId);

  xsResetTaskAmount();
}

// 15 - Effect of Paper Money for Vietnamese
void EffectFunction15(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeChoppingGoldProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
  xsTaskAmount(cTaskAttrSearchWaitTime, 3);
  xsTaskAmount(cTaskAttrAutoSearch, 1);
  xsTaskAmount(cTaskAttrEnableTargeting, 1);
  xsTaskAmount(cTaskAttrOwnerType, 5);
  xsTaskAmount(cTaskAttrGatherType, 1);

  xsTask(LumberjackMaleID, cTaskTypeGenerateResources, cTreeClass, playerId);
  xsTask(LumberjackFemaleID, cTaskTypeGenerateResources, cTreeClass, playerId);

  xsResetTaskAmount();
}

// 16 - Effect of Lumberjack Bonus for Shu/Athenians
void EffectFunction16(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeChoppingFoodProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);

  xsTask(LumberjackMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(LumberjackFemaleID, cTaskTypeAdditionalResource, -1, playerId);

  xsResetTaskAmount();
}

// Add Curare effect
void Curare(int UnitTarget = -1, int playerId = -1)
{
  xsEffectAmount(cAddAttribute, UnitTarget, cCombatAbility, 128, playerId);
  xsModifyObjectTasks(UnitTarget, playerId, 0);
}

// Remove Curare from undesirable units
void CurareRemoval(int UnitTarget = -1, int playerId = -1)
{
  xsEffectAmount(cAddAttribute, UnitTarget, cCombatAbility, -128, playerId);
  xsModifyObjectTasks(UnitTarget, playerId, -1);
}

// 25 - Add Curare for Tupi
void EffectFunction25(int playerId = -1)
{
  int TargetClass = 0;

  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue2, 15);
  xsTaskAmount(cTaskAttrSearchWaitTime, 109);
  xsTaskAmount(cTaskAttrWorkRange, 1);
  TargetClass = cFlagClassRemoval * (cFlagClassOffset + cFlagClassBuilding + cFlagClassSiege + cFlagClassShip);

  xsTaskAmount(cTaskAttrObjectClass, TargetClass); // All except Buildings, Ships and Siege
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeStinger);
  xsTaskAmount(cTaskAttrWorkValue1, -20);

  Curare(cArcherClass, playerId);

  CurareRemoval(SkirmisherID, playerId);
  CurareRemoval(EliteSkirmisherID, playerId);
  CurareRemoval(ImperialSkirmisherID, playerId);
  CurareRemoval(GuechaWarriorID, playerId);
  CurareRemoval(EliteGuechaWarriorID, playerId);
  CurareRemoval(SlingerID, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, -8);
  xsModifyObjectTasks(BlackWoodArcherID, playerId, 0, true);
  xsModifyObjectTasks(EliteBlackWoodArcherID, playerId, 0, true);

  xsTaskAmount(cTaskAttrWorkValue1, -30);
  Curare(cBuildingClass, playerId);
  Curare(cTowerClass, playerId);

  Curare(TownCenterProjID, playerId);
  Curare(TownCenterFireProjID, playerId);
  Curare(TowerProjID, playerId);
  Curare(TowerFireProjID, playerId);
  Curare(CastleProjID, playerId);
  Curare(CastleFireProjID, playerId);
  Curare(KrepostProjID, playerId);
  Curare(KrepostFireProjID, playerId);
  Curare(ProjectileDockID, playerId);
  Curare(ProjectileDockFireID, playerId);
  Curare(ProjectileChurchID, playerId);

  xsResetTaskAmount();
}

// 26 - Effect of Cavalry kill for Mapuche
void EffectFunction26(int playerId = -1)
{
  int TargetClass = 0;
  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue1, 3);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

  TargetClass = cFlagClassRemoval * (cFlagClassOffset + cFlagClassBuilding + cFlagClassCivilian);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass); // All except Buildings and Workers
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeLoot);

  xsModifyObjectTasks(cCavalryClass, playerId, 0);
  xsModifyObjectTasks(cScoutCavalryClass, playerId, 0);
  xsModifyObjectTasks(cConquistadorClass, playerId, 0);
  xsModifyObjectTasks(cCavalryArcherClass, playerId, 0);

  xsTaskAmount(cTaskAttrWorkValue1, -3);
  xsTaskAmount(cTaskAttrObjectClass, cTradeBoatClass);
  xsModifyObjectTasks(cCavalryClass, playerId, 0);
  xsModifyObjectTasks(cScoutCavalryClass, playerId, 0);
  xsModifyObjectTasks(cConquistadorClass, playerId, 0);
  xsModifyObjectTasks(cCavalryArcherClass, playerId, 0);

  xsTaskAmount(cTaskAttrObjectClass, cFishingBoatClass);
  xsModifyObjectTasks(cCavalryClass, playerId, 0);
  xsModifyObjectTasks(cScoutCavalryClass, playerId, 0);
  xsModifyObjectTasks(cConquistadorClass, playerId, 0);
  xsModifyObjectTasks(cCavalryArcherClass, playerId, 0);

  xsResetTaskAmount();
}

// Apply Cost Refund for Tupis
void TupiRefund(int TaskID = -1, int playerId = -1)
{
  xsTask(cVillagerClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cArcherClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cInfantryClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cCavalryClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cMonkClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cTradeCartClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cConquistadorClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cPetardClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cCavalryArcherClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cMonkWithRelicClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cHandCannoneerClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cScoutCavalryClass, cTaskTypeRefund, TaskID, playerId);
}

// 27 - Effect of Unit Refund for Tupis
void EffectFunction27(int playerId = -1)
{
  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue1, 1);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeUnitCostRefund);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  TupiRefund(-1, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);
  TupiRefund(-2, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeWood);
  TupiRefund(-3, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 0.5);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  xsTask(BlackWoodArcherID, cTaskTypeRefund, -1, playerId);
  xsTask(EliteBlackWoodArcherID, cTaskTypeRefund, -1, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);
  xsTask(BlackWoodArcherID, cTaskTypeRefund, -2, playerId);
  xsTask(EliteBlackWoodArcherID, cTaskTypeRefund, -2, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeWood);
  xsTask(BlackWoodArcherID, cTaskTypeRefund, -3, playerId);
  xsTask(EliteBlackWoodArcherID, cTaskTypeRefund, -3, playerId);
  xsResetTaskAmount();
}

// Apply Settlement Healing For Muisca
void MuiscaHeal(int HealAmount = -1, int SettlementAge = -1, int playerId = -1)
{
  xsTaskAmount(cTaskAttrWorkValue1, HealAmount);
  xsEffectAmount(cAddAttribute, SettlementAge, cCombatAbility, 32, playerId);
  xsModifyObjectTasks(SettlementAge, playerId, 0);
}

// 28 - Effect of Settlements for Muisca Feudal & Castle Age
void EffectFunction28(int playerId = -1)
{
  int TargetClass = 0;
  xsResetTaskAmount();

  TargetClass = cFlagClassRemoval * (cFlagClassOffset + cFlagClassBuilding + cFlagClassShip + cFlagClassSiege);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass); // All except Buildings, Siege and Ships
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeAura);

  xsTaskAmount(cTaskAttrWorkValue2, 1);
  xsTaskAmount(cTaskAttrWorkRange, 3);
  xsTaskAmount(cTaskAttrGatheringSoundInt32, 13407);
  xsTaskAmount(cTaskAttrDepositSoundInt32, 13407);
  xsTaskAmount(cTaskAttrOwnerType, 4);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 4);
  xsTaskAmount(cTaskAttrSearchWaitTime, 109);
  xsTaskAmount(cTaskAttrGatherType, 21);

  xsModifyObjectTasks(cCavalryClass, playerId, 0);

  MuiscaHeal(5, Settlement1ID, playerId);
  MuiscaHeal(10, Settlement2ID, playerId);
  MuiscaHeal(15, Settlement3ID, playerId);

  xsResetTaskAmount();
}

// 29 - Effect of Forager Bonus for Mapuche
void EffectFunction29(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeExtraForageProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);

  xsTask(ForagerMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ForagerFemaleID, cTaskTypeAdditionalResource, -1, playerId);

  xsResetTaskAmount();
}

// 30 - Effect of Hamask for Danes
void EffectFunction30(int playerId = -1)
{
  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue1, 1);
  xsTaskAmount(cTaskAttrWorkValue2, 0.1);
  xsTaskAmount(cTaskAttrWorkRange, 0);
  xsTask(cInfantryClass, 160, -1, playerId);
  xsTask(cInfantryClass, 160, cBuildingClass, playerId);
  xsTask(cInfantryClass, 160, cWallClass, playerId);
  xsTask(cInfantryClass, 160, cGateClass, playerId);
  xsTask(cInfantryClass, 160, cFarmClass, playerId);
}

// 31 - Effect of Shield Wall for Saxons
void EffectFunction31(int playerId = -1)
{
  xsEffectAmount(cAddAttribute, cInfantryClass, cCombatAbility, 96, playerId);
  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue1, 3);
  xsTaskAmount(cTaskAttrWorkValue2, 44);
  xsTaskAmount(cTaskAttrWorkRange, 7);
  xsTaskAmount(cTaskAttrGatheringSoundInt32, 13411);
  xsTaskAmount(cTaskAttrDepositSoundInt32, 13411);
  xsTaskAmount(cTaskAttrOwnerType, 1);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 2);
  xsTaskAmount(cTaskAttrSearchWaitTime, 116);
  xsTaskAmount(cTaskAttrAutoSearch, 0);
  xsTask(cInfantryClass, cTaskTypeAura, cInfantryClass, playerId);
  xsTaskAmount(cTaskAttrSearchWaitTime, 117);
  xsTaskAmount(cTaskAttrAutoSearch, 1);
  xsTask(cInfantryClass, cTaskTypeAura, cInfantryClass, playerId);
}

// 32 - Effect of Gothikon for Varangians
void EffectFunction32(int playerId = -1)
{
  int TargetClass = 0;

  xsEffectAmount(cAddAttribute, VarangianGuardID, cCombatAbility, 128, playerId);
  xsEffectAmount(cAddAttribute, EliteVarangianGuardID, cCombatAbility, 128, playerId);

  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue1, 1.5);
  xsTaskAmount(cTaskAttrWorkValue2, 1.6);
  xsTaskAmount(cTaskAttrSearchWaitTime, 120);

  TargetClass = cFlagClassRemoval * (cFlagClassOffset + cFlagClassBuilding);
  xsTaskAmount(cTaskAttrObjectClass, TargetClass); // All except Buildings
  xsTaskAmount(cTaskAttrTaskType, cTaskTypeStinger);

  xsModifyObjectTasks(VarangianGuardID, playerId, 0);
  xsModifyObjectTasks(EliteVarangianGuardID, playerId, 0);
}

// 34 - Effect of Fishing Ships, Hunters, Shepherds bonus for Varangians
void EffectFunction34(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrProductivityResource, cAttributeButcherGoldProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  xsTaskAmount(cTaskAttrWorkValue1, 0.01);

  xsTask(HunterMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(HunterFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ShepherdMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ShepherdFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(FishermanMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(FishermanFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTaskAmount(cTaskAttrWorkValue1, 0.005);
  xsTask(cFishingBoatClass, cTaskTypeAdditionalResource, -1, playerId);
}


// 35 - Effect of Farmer bonus for Danes
void EffectFunction35(int playerId = -1)
{
  xsTaskAmount(cTaskAttrWorkValue1, 0.01);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeExtraFoodProductivity);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);

  xsTask(FarmerMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(FarmerFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(FishermanMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(FishermanFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ForagerMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(HunterMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(HunterFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ForagerFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ShepherdMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(ShepherdFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(HerderMaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(HerderFemaleID, cTaskTypeAdditionalResource, -1, playerId);
  xsTask(FishingShipID, cTaskTypeAdditionalResource, -1, playerId);

  xsResetTaskAmount();
}

// Apply Pillage for Danes
void PillageBuildings(int TaskID = -1, int playerId = -1)
{
  xsTask(cBuildingClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cFarmClass, cTaskTypeRefund, TaskID, playerId);
  xsTask(cTowerClass, cTaskTypeRefund, TaskID, playerId);
}

// 36 - Effect of Pillage bonus for Danes
void EffectFunction36(int playerId = -1)
{
  xsResetTaskAmount();
  xsTaskAmount(cTaskAttrWorkValue1, 0.001);
  xsTaskAmount(cTaskAttrProductivityResource, cAttributeRazingPillage);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
  xsTaskAmount(cTaskAttrWorkRange, 1);
  xsTaskAmount(cTaskAttrOwnerType, 5);
  xsTaskAmount(cTaskAttrGatherType, 10);

  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
  PillageBuildings(-1, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);
  PillageBuildings(-2, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeWood);
  PillageBuildings(-3, playerId);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeStone);
  PillageBuildings(-4, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 0.1);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 0);
  xsTask(TownCenterFnd1ID, cTaskTypeRefund, -4, playerId);
  xsTask(TownCenterFnd2ID, cTaskTypeRefund, -4, playerId);
  xsTask(TownCenterFnd3ID, cTaskTypeRefund, -4, playerId);
  xsTask(TownCenterFnd4ID, cTaskTypeRefund, -4, playerId);
  xsResetTaskAmount();
}

// 38 - Effect of Fyrd Discount for Saxons
void EffectFunction38(int playerId = -1)
{
  int NewLevel = xsPlayerAttribute(playerId, cAttributeInfantryFyrdLevel);
  float DiscountMul = 0.9425;

  if ((NewLevel <= 4) && (NewLevel > 0))
    {
    xsEffectAmount(cMulAttribute, cInfantryClass, cResourceCost, DiscountMul, playerId);
    xsEffectAmount(cMulAttribute, cArcherClass, cResourceCost, DiscountMul, playerId);
    xsEffectAmount(cMulAttribute, cHandCannoneerClass, cResourceCost, DiscountMul, playerId);

    }
}

// 39 - Second Effect of Fyrd Discount for Saxons
void EffectFunction39(int playerId = -1)
{
  int NewLevel = xsPlayerAttribute(playerId, cAttributeInfantryFyrdLevel);
  float DiscountMul = 1.0614;

  if ((NewLevel < 4) && (NewLevel >= 0))
    {
    xsEffectAmount(cMulAttribute, cInfantryClass, cResourceCost, DiscountMul, playerId);
    xsEffectAmount(cMulAttribute, cArcherClass, cResourceCost, DiscountMul, playerId);
    xsEffectAmount(cMulAttribute, cHandCannoneerClass, cResourceCost, DiscountMul, playerId);

    }
}

void patchKhmerNoDropsite(int playerId = -1, int objectId = -1)
{
  for(taskId = 0; < xsGetObjectTaskCount(objectId, playerId))
  {
      xsObjectTaskAmount(objectId, playerId, taskId);
      // xsc-ignore: NumDownCast
      int taskType = xsGetTaskAmount(cTaskAttrTaskType);
      if(taskType == cTaskTypeGatherRebuild)
      {
          xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
          xsModifyObjectTasks(objectId, playerId, taskId, true);
      }
  }
}

// 50 - Effect of Farm Bonus for Khmer
void EffectFunction50(int playerId = -1)
{
  xsResetTaskAmount();
  patchKhmerNoDropsite(playerId, FarmerMaleID);
  patchKhmerNoDropsite(playerId, FarmerFemaleID);
  xsResetTaskAmount();
}

bool Effects_isCastleUniqueUnit(int objectId = -1)
{
    // xsc-ignore: NumDownCast
    int trainLoc = xsGetObjectAttribute(cGaia, objectId, cTrainLocation);
    // xsc-ignore: NumDownCast
    int trainButton = xsGetObjectAttribute(cGaia, objectId, cTrainButton);
    // xsc-ignore: NumDownCast
    int armor = xsGetObjectAttribute(cGaia, objectId, cArmor, cDamageClassUniqueUnits);
    // xsc-ignore: NumDownCast
    int heroStatus = xsGetObjectAttribute(cGaia, objectId, cHeroStatus);

    return (
        trainLoc == CastleID
        && (trainButton == 0 || trainButton == 1)
        && armor != -1
        && (heroStatus == 0 || heroStatus == 2)
         || objectId == SunJianID
        || objectId == CaoCaoID
        || objectId == LiuBeiID
    );
}

// Display Message for special Technologies
void Effects_DisplayTechNotification(int messageString = -1, int unitIcon = -1, string soundEvent = "", int validDiplomacies = -1, int playerId = -1)
{
    string playerName = xsGetPlayerName(playerId);
    string color = xsGetPlayerColorTag(playerId);
    string msg = xsGetString(messageString, true);

    for(player = 1; <= xsGetNumPlayers())
    {
        int currentDiplomacy = xsGetDiplomacy(playerId, player);
        // Check if the current diplomacy is inside the validDiplomacies array
        for(i = 0; < xsArrayGetSize(validDiplomacies))
        {
            if(currentDiplomacy == xsArrayGetInt(validDiplomacies, i))
            {
                xsDisplayInstructions(
                    xsGetPlayerColorTag(playerId) + fstr(msg),
                    15,
                    playerId,
                    unitIcon,
                    cPanelTop,
                    true,
                    true,
                    soundEvent,
                    player
                );
                break;
            }
        }
    }
}


// 51 - Effect of Butalmapu for Mapuche
void EffectFunction51(int playerId = -1)
{
  int messageString = 3138;
  string soundEvent = "?trumpet";
  int ValidDiplomacies = xsArrayCreateInt(1);
  float UnitDiscount = 0.85;
  xsArraySetInt(ValidDiplomacies, 1, cDiplomacyAlly);

  Effects_DisplayTechNotification(messageString, EliteKonaID, soundEvent, ValidDiplomacies, playerId);

  for(objectId = 0; <= xsGetPlayerNumberOfObjects(playerId))
  {
    if(Effects_isCastleUniqueUnit(objectId) == true)
    {
        for(player = 1; <= xsGetNumPlayers())
        {
          int currentDiplomacy = xsGetDiplomacy(playerId, player);
          if(currentDiplomacy == cDiplomacyAlly)
          {
            xsEffectAmount(cMulAttribute, objectId, cResourceCost, UnitDiscount, player);
          }
        }
    }
  }
}

// 52 - Effect of Kasbah for Berbers
void EffectFunction52(int playerId = -1)
{
  int messageString = 3139;
  string soundEvent = "?reform";
  int ValidDiplomacies = xsArrayCreateInt(1);
  xsArraySetInt(ValidDiplomacies, 1, cDiplomacyAlly);

  Effects_DisplayTechNotification(messageString, CastleID, soundEvent,  ValidDiplomacies, playerId);
}

// 53 - Effect of Cuman Mercenaries for Cumans
void EffectFunction53(int playerId = -1)
{
  int messageString = 3132;
  string soundEvent = "?mercenaries";
  int ValidDiplomacies = xsArrayCreateInt(1);
  xsArraySetInt(ValidDiplomacies, 1, cDiplomacyAlly);

  Effects_DisplayTechNotification(messageString, EliteKipchakID, soundEvent,  ValidDiplomacies, playerId);
}

// 54 - Effect of First Crusade for Sicilians
void EffectFunction54(int playerId = -1)
{
  int messageString = 3130;
  string soundEvent = "?crusades";
  int ValidDiplomacies = xsArrayCreateInt(4);
  xsArraySetInt(ValidDiplomacies, 0, cDiplomacyAlly);
  xsArraySetInt(ValidDiplomacies, 1, cDiplomacyEnemy);
  xsArraySetInt(ValidDiplomacies, 2, cDiplomacyNeutral);
  xsArraySetInt(ValidDiplomacies, 3, cDiplomacyTreaty);

  Effects_DisplayTechNotification(messageString, EliteSerjeantID, soundEvent,  ValidDiplomacies, playerId);
}

// 55 - Effect of Flemish Revolution for Burgundians
void EffectFunction55(int playerId = -1)
{
  int messageString = 3131;
  string soundEvent = "?revolution";
  int ValidDiplomacies = xsArrayCreateInt(4);
  xsArraySetInt(ValidDiplomacies, 0, cDiplomacyAlly);
  xsArraySetInt(ValidDiplomacies, 1, cDiplomacyEnemy);
  xsArraySetInt(ValidDiplomacies, 2, cDiplomacyNeutral);
  xsArraySetInt(ValidDiplomacies, 3, cDiplomacyTreaty);

  Effects_DisplayTechNotification(messageString, FlemishMilitiaID, soundEvent,  ValidDiplomacies, playerId);
}

// 56 - Effect of Atheism for Huns
void EffectFunction56(int playerId = -1)
{
  int messageString = 3118;
  if (xsGetVictoryType() == cVictoryTypeConquest)
  {
    messageString = 3140;
  }
  string soundEvent = "?atheism";
  int ValidDiplomacies = xsArrayCreateInt(4);
  xsArraySetInt(ValidDiplomacies, 0, cDiplomacyAlly);
  xsArraySetInt(ValidDiplomacies, 1, cDiplomacyEnemy);
  xsArraySetInt(ValidDiplomacies, 2, cDiplomacyNeutral);
  xsArraySetInt(ValidDiplomacies, 3, cDiplomacyTreaty);

  Effects_DisplayTechNotification(messageString, EliteTarkanID, soundEvent,  ValidDiplomacies, playerId);
}

// Chronicles

void OdomantianRaiderHighValueTargets(int taskObject = -1, int playerId = -1)
{
  xsTask(taskObject, cTaskTypeLoot, cTradeBoatClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cVillagerClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cTradeCartClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cMonkWithRelicClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cMonkClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cMonkWithRelicClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cKingClass, playerId);
}

void OdomantianRaiderLowValueTargets(int taskObject = -1, int playerId = -1)
{
  xsTask(taskObject, cTaskTypeLoot, cArcherClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cInfantryClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cCavalryClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cSiegeWeaponClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cArcherClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cTransportShipClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cWarshipClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cConquistadorClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cPetardClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cCavalryArcherClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cHandCannoneerClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cScoutCavalryClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cPackedUnitClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cUnpackedSiegeUnitClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cScorpionClass, playerId);
}

// 1000 - Effect of Odomantian Raiders for Thracians
void EffectFunction1000(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 5);
  xsTaskAmount(cTaskAttrProductivityResource, 510);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

  OdomantianRaiderHighValueTargets(cInfantryClass, playerId);
  OdomantianRaiderHighValueTargets(cCavalryClass, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 3);

  OdomantianRaiderLowValueTargets(cInfantryClass, playerId);
  OdomantianRaiderLowValueTargets(cCavalryClass, playerId);

  xsResetTaskAmount();
}

void AthenianMilitaryPolicy(int taskObject = -1, int playerId = -1)
{
  xsTask(taskObject, cTaskTypeLoot, cTradeBoatClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cVillagerClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cTradeCartClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cMonkWithRelicClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cMonkClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cMonkWithRelicClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cKingClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cArcherClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cInfantryClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cCavalryClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cSiegeWeaponClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cArcherClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cTransportShipClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cWarshipClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cConquistadorClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cPetardClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cCavalryArcherClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cHandCannoneerClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cScoutCavalryClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cPackedUnitClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cUnpackedSiegeUnitClass, playerId);
  xsTask(taskObject, cTaskTypeLoot, cScorpionClass, playerId);
}

// 1001 - Effect of Military Policy for Athenians
void EffectFunction1001(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 3);
  xsTaskAmount(cTaskAttrProductivityResource, 551);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

  AthenianMilitaryPolicy(cInfantryClass, playerId);
  AthenianMilitaryPolicy(cCavalryClass, playerId);
  AthenianMilitaryPolicy(cScoutCavalryClass, playerId);
  AthenianMilitaryPolicy(MonoremeID, playerId);
  AthenianMilitaryPolicy(BiremeID, playerId);
  AthenianMilitaryPolicy(TriremeID, playerId);

  xsResetTaskAmount();
}

void ApplyPuruRegenAbility(int targetObject = -1, int playerId = -1)
{
  xsEffectAmount(cAddAttribute, targetObject, cCombatAbility, 96, playerId);
  xsEffectAmount(cAddAttribute, targetObject, cRegenerationRate, 25, playerId);

  xsTaskAmount(cTaskAttrAutoSearch, 0);

  xsTask(targetObject, cTaskTypeAura, cTradeBoatClass, playerId);

  xsTaskAmount(cTaskAttrAutoSearch, 1);

  xsTask(targetObject, cTaskTypeAura, cVillagerClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cTradeCartClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cMonkWithRelicClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cMonkClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cMonkWithRelicClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cKingClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cArcherClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cInfantryClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cCavalryClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cSiegeWeaponClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cArcherClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cTransportShipClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cWarshipClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cConquistadorClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cPetardClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cCavalryArcherClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cHandCannoneerClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cScoutCavalryClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cPackedUnitClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cUnpackedSiegeUnitClass, playerId);
  xsTask(targetObject, cTaskTypeAura, cScorpionClass, playerId);
}

// 1002 - Apply regeneration with no enemies nearby for Puru
void EffectFunction1002(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, -25);
  xsTaskAmount(cTaskAttrWorkValue2, 1);
  xsTaskAmount(cTaskAttrWorkRange, 10);
  xsTaskAmount(cTaskAttrOwnerType, 1);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 130);
  xsTaskAmount(cTaskAttrSearchWaitTime, 109);
  xsTaskAmount(cTaskAttrOwnerType, 5);

  xsTask(cCavalryClass, cTaskTypeAura, cTradeBoatClass, playerId);

  xsTaskAmount(cTaskAttrAutoSearch, 1);

  ApplyPuruRegenAbility(cCavalryClass, playerId);
  ApplyPuruRegenAbility(cScoutCavalryClass, playerId);

  xsResetTaskAmount();
}

// 1003 - Effect of Dii Plunderers for Thracians
void EffectFunction1003(int playerId = -1)
{
  xsResetTaskAmount();

  xsTaskAmount(cTaskAttrWorkValue1, 0.15);
  xsTaskAmount(cTaskAttrProductivityResource, 511);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeWood);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
  xsTaskAmount(cTaskAttrSearchWaitTime, 3);
  xsTaskAmount(cTaskAttrAutoSearch, 1);
  xsTaskAmount(cTaskAttrEnableTargeting, 1);
  xsTaskAmount(cTaskAttrOwnerType, 5);
  xsTaskAmount(cTaskAttrGatherType, 1);

  xsTask(SpearmanID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(PikemanID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(HalberdierID, cTaskTypeGenerateResources, cBuildingClass, playerId);

  xsTaskAmount(cTaskAttrResourceOut, cAttributeFood);

  xsTask(MilitiaID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(ManAtArmsID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(LongSwordsmanID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(ChampionID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(HopliteID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(EliteHopliteID, cTaskTypeGenerateResources, cBuildingClass, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 0.1);
  xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

  xsTask(RhomphaiaWarriorID, cTaskTypeGenerateResources, cBuildingClass, playerId);
  xsTask(EliteRhomphaiaWarriorID, cTaskTypeGenerateResources, cBuildingClass, playerId);

  xsResetTaskAmount();
}

// 1004 - Apply Thracians Tower Workrate Bonus
void EffectFunction1004(int playerId = -1)
{
  xsResetTaskAmount();

  xsEffectAmount(cAddAttribute, cTowerClass, cCombatAbility, 32, playerId);

  xsTaskAmount(cTaskAttrWorkValue1, 0.15);
  xsTaskAmount(cTaskAttrWorkValue2, 1);
  xsTaskAmount(cTaskAttrWorkRange, 8);
  xsTaskAmount(cTaskAttrOwnerType, 1);
  xsTaskAmount(cTaskAttrCombatLevelFlag, 5);
  xsTaskAmount(cTaskAttrSearchWaitTime, 13);

  xsTask(cTowerClass, cTaskTypeAura, LumberjackMaleID, playerId);
  xsTask(cTowerClass, cTaskTypeAura, StoneMinerMaleID, playerId);
  xsTask(cTowerClass, cTaskTypeAura, LumberjackFemaleID, playerId);
  xsTask(cTowerClass, cTaskTypeAura, StoneMinerFemaleID, playerId);
  xsTask(cTowerClass, cTaskTypeAura, GoldMinerMaleID, playerId);
  xsTask(cTowerClass, cTaskTypeAura, GoldMinerFemaleID, playerId);

  xsResetTaskAmount();
}


include "custom-constants.xs";
include "custom-effects.xs";