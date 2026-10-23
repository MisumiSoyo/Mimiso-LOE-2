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
    DetinetsApplier(playerId, CastleID);
    DetinetsApplier(playerId, WatchTowerID);
    DetinetsApplier(playerId, GuardTowerID);
    DetinetsApplier(playerId, KeepID);
    DetinetsApplier(playerId, BombardTowerID);
    DetinetsApplier(playerId, KrepostID);
    DetinetsApplier(playerId, DonjonID);
}



void main()
{
    xsChatData("Mod: Legacy of Empires 2");
    xsChatData("Patch: 0.8  2026.10.24");
    xsChatData("Author: Misumi Soyo");
}