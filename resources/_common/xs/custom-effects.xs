include "array.xs";
include "math.xs";
include "ability.xs";



//  10001 - Corvinian Army
void EffectFunction10001(int playerId = -1)
{
    CorvinianArmyApplier(playerId, MagyarHuszarID);
    CorvinianArmyApplier(playerId, EliteMagyarHuszarID);
    CorvinianArmyApplier(playerId, LOEEarlyMagyarHuszarID);
}



//  10002 - Detinets
void EffectFunction10002(int playerId = -1)
{
    DetinetsObjectApplier(playerId, CastleID);
    DetinetsObjectApplier(playerId, KrepostID);
    DetinetsObjectApplier(playerId, DonjonID);
    DetinetsTechApplier(playerId, GuardTowerTechID);
    DetinetsTechApplier(playerId, KeepTechID);
    DetinetsTechApplier(playerId, BombardTowerTechID);
}



//  10003 - Paper Money
void EffectFunction10003(int playerId = -1)
{
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrSearchWaitTime, 1001);
    xsTaskAmount(cTaskAttrWorkValue1, 0.01);
    xsTaskAmount(cTaskAttrProductivityResource, LOEAttrPaperMoney);
    xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);

    xsTask(MaleLumberjackID, cTaskTypeAdditionalResource, -1, playerId);
    xsTask(FemaleLumberjackID, cTaskTypeAdditionalResource, -1, playerId);
    xsResetTaskAmount();
}



void main()
{
    xsChatData("Mod: Legacy of Empires 2");
    xsChatData("Patch: 0.10  2026.10.25");
    xsChatData("Author: Misumi Soyo");
}