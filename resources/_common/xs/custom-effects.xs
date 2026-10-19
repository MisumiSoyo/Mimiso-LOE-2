include "array.xs";
include "math.xs";
include "ability.xs";



//  10001 - Two-Man Saw
void EffectFunction10001(int playerId = -1)
{
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrSearchWaitTime, 1001);
    xsTaskAmount(cTaskAttrWorkValue1, 0.01);
    xsTaskAmount(cTaskAttrResourceOut, cAttributeWood);
    xsTaskAmount(cTaskAttrProductivityResource, LOEAttrExtraWood);

    xsTask(MaleLumberjackID, cTaskTypeAdditionalResource, -1, playerId);
    xsTask(FemaleLumberjackID, cTaskTypeAdditionalResource, -1, playerId);
    xsResetTaskAmount();
    ModResource(playerId, LOEAttrExtraWood, 15);
}



//  10002 - Cupellation
void EffectFunction10002(int playerId = -1)
{
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrSearchWaitTime, 1002);
    xsTaskAmount(cTaskAttrWorkValue1, 0.01);
    xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
    xsTaskAmount(cTaskAttrProductivityResource, LOEAttrExtraGold);

    xsTask(MaleGoldMinerID, cTaskTypeAdditionalResource, -1, playerId);
    xsTask(FemaleGoldMinerID, cTaskTypeAdditionalResource, -1, playerId);
    xsResetTaskAmount();
    ModResource(playerId, LOEAttrExtraGold, 25);
}



void main()
{
    xsChatData("Mod: Legacy of Empires 2");
    xsChatData("Patch: 0.2  2026.10.19");
    xsChatData("Author: Misumi Soyo");
}