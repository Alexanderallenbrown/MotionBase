#include "__cf_demostration.h"
#if 0
This file is not available for use in any application other than as a MATLAB
( R ) MEX file for use with the Simulink ( R ) product . If you do not have
the Simulink Coder licensed , this file contains encrypted block names , etc
. If you purchase the Simulink Coder , this file will contain full block
descriptions and improved variable names .
#endif
#include <math.h>
#include "demostration_acc.h"
#include "demostration_acc_private.h"
#include <stdio.h>
#include "slexec_vm_simstruct_bridge.h"
#include "slexec_vm_zc_functions.h"
#include "simstruc.h"
#include "fixedpoint.h"
#define CodeFormat S-Function
#define AccDefine1 Accelerator_S-Function
static void mdlOutputs ( SimStruct * S , int_T tid ) { real_T currentTime ;
htmb1f42yb * _rtB ; aa5zavtgxb * _rtP ; bxkf2zvmyy * _rtX ; mpt0mzz342 *
_rtDW ; _rtDW = ( ( mpt0mzz342 * ) ssGetRootDWork ( S ) ) ; _rtX = ( (
bxkf2zvmyy * ) ssGetContStates ( S ) ) ; _rtP = ( ( aa5zavtgxb * )
ssGetDefaultParam ( S ) ) ; _rtB = ( ( htmb1f42yb * ) _ssGetBlockIO ( S ) ) ;
_rtB -> oo3zkbgchn = ssGetT ( S ) ; if ( ssIsSampleHit ( S , 2 , 0 ) ) {
ssCallAccelRunBlock ( S , 0 , 1 , SS_CALL_MDL_OUTPUTS ) ; } _rtB ->
ngnykszfkn = 0.0 ; _rtB -> ngnykszfkn += _rtP -> P_1 [ 0 ] * _rtX ->
nas0omrfkh [ 0 ] ; _rtB -> ngnykszfkn += _rtP -> P_1 [ 1 ] * _rtX ->
nas0omrfkh [ 1 ] ; if ( ssIsSampleHit ( S , 3 , 0 ) ) { _rtB -> agov32gnlp =
_rtP -> P_2 * _rtB -> ngnykszfkn ; ssCallAccelRunBlock ( S , 0 , 4 ,
SS_CALL_MDL_OUTPUTS ) ; } _rtB -> bt0necdsl4 = _rtX -> c53qp3dtca ;
ssCallAccelRunBlock ( S , 0 , 6 , SS_CALL_MDL_OUTPUTS ) ; if ( ssIsSampleHit
( S , 2 , 0 ) ) { ssCallAccelRunBlock ( S , 0 , 7 , SS_CALL_MDL_OUTPUTS ) ;
ssCallAccelRunBlock ( S , 0 , 8 , SS_CALL_MDL_OUTPUTS ) ; ssCallAccelRunBlock
( S , 0 , 9 , SS_CALL_MDL_OUTPUTS ) ; } if ( ssIsSampleHit ( S , 1 , 0 ) ) {
currentTime = ssGetTaskTime ( S , 1 ) ; _rtDW -> jvlh1y55xk = ( currentTime
>= _rtP -> P_4 ) ; if ( _rtDW -> jvlh1y55xk == 1 ) { _rtB -> nbfc4ardpk =
_rtP -> P_6 ; } else { _rtB -> nbfc4ardpk = _rtP -> P_5 ; }
ssCallAccelRunBlock ( S , 0 , 11 , SS_CALL_MDL_OUTPUTS ) ; } if (
ssIsSampleHit ( S , 3 , 0 ) ) { _rtB -> ek5nd0wwac = _rtP -> P_7 * _rtB ->
dbqplcxyib ; } _rtB -> mqjbxnvs0a = _rtX -> peewifpgt1 ; _rtB -> oqtkmx5vce =
0.0 ; _rtB -> oqtkmx5vce += _rtP -> P_10 [ 0 ] * _rtX -> hcymlbn1pk [ 0 ] ;
_rtB -> oqtkmx5vce += _rtP -> P_10 [ 1 ] * _rtX -> hcymlbn1pk [ 1 ] ; _rtB ->
oqtkmx5vce += _rtP -> P_11 * _rtB -> ek5nd0wwac ; _rtB -> fo12xfqqwn = _rtX
-> hakkqyygmj ; ssCallAccelRunBlock ( S , 0 , 16 , SS_CALL_MDL_OUTPUTS ) ;
_rtB -> ntppihowe3 = _rtX -> aurwnltqa2 ; ssCallAccelRunBlock ( S , 0 , 18 ,
SS_CALL_MDL_OUTPUTS ) ; if ( ssIsSampleHit ( S , 2 , 0 ) ) {
ssCallAccelRunBlock ( S , 0 , 19 , SS_CALL_MDL_OUTPUTS ) ; } if (
ssIsSampleHit ( S , 1 , 0 ) ) { currentTime = ssGetTaskTime ( S , 1 ) ; _rtDW
-> b1jbfgocjd = ( currentTime >= _rtP -> P_14 ) ; if ( _rtDW -> b1jbfgocjd ==
1 ) { _rtB -> nbfc4ardpk = _rtP -> P_16 ; } else { _rtB -> nbfc4ardpk = _rtP
-> P_15 ; } ssCallAccelRunBlock ( S , 0 , 21 , SS_CALL_MDL_OUTPUTS ) ; } if (
ssIsSampleHit ( S , 3 , 0 ) ) { _rtB -> ik34kg002i = _rtP -> P_17 * _rtB ->
mvdfc0tvgf ; } _rtB -> kkns3oxlmq = 0.0 ; _rtB -> kkns3oxlmq += _rtP -> P_19
[ 0 ] * _rtX -> p0mh0ay1l4 [ 0 ] ; _rtB -> kkns3oxlmq += _rtP -> P_19 [ 1 ] *
_rtX -> p0mh0ay1l4 [ 1 ] ; _rtB -> kkns3oxlmq += _rtP -> P_20 * _rtB ->
ik34kg002i ; ssCallAccelRunBlock ( S , 0 , 24 , SS_CALL_MDL_OUTPUTS ) ; _rtB
-> baqvkhbwgz = 0.0 ; _rtB -> baqvkhbwgz += _rtP -> P_22 [ 0 ] * _rtX ->
gytq4zwpra [ 0 ] ; _rtB -> baqvkhbwgz += _rtP -> P_22 [ 1 ] * _rtX ->
gytq4zwpra [ 1 ] ; _rtB -> ktd4mv1rkx = _rtB -> kkns3oxlmq + _rtB ->
baqvkhbwgz ; ssCallAccelRunBlock ( S , 0 , 27 , SS_CALL_MDL_OUTPUTS ) ;
ssCallAccelRunBlock ( S , 0 , 28 , SS_CALL_MDL_OUTPUTS ) ; if ( ssIsSampleHit
( S , 3 , 0 ) ) { currentTime = _rtP -> P_23 * _rtB -> baqvkhbwgz ; if (
currentTime > 1.0 ) { currentTime = 1.0 ; } else { if ( currentTime < - 1.0 )
{ currentTime = - 1.0 ; } } _rtB -> cwmw2kpa4g = muDoubleScalarAsin (
currentTime ) ; } if ( ssIsSampleHit ( S , 2 , 0 ) ) { ssCallAccelRunBlock (
S , 0 , 31 , SS_CALL_MDL_OUTPUTS ) ; ssCallAccelRunBlock ( S , 0 , 32 ,
SS_CALL_MDL_OUTPUTS ) ; } _rtB -> afrib3w5oq = _rtX -> bjdkmyv0ro ;
ssCallAccelRunBlock ( S , 0 , 34 , SS_CALL_MDL_OUTPUTS ) ; if ( ssIsSampleHit
( S , 2 , 0 ) ) { ssCallAccelRunBlock ( S , 0 , 35 , SS_CALL_MDL_OUTPUTS ) ;
ssCallAccelRunBlock ( S , 0 , 36 , SS_CALL_MDL_OUTPUTS ) ; } if (
ssIsSampleHit ( S , 3 , 0 ) ) { _rtB -> apx33sizl1 = _rtP -> P_25 * _rtB ->
gg1eu0r4ea ; } _rtB -> mdedgzboxv = _rtX -> psl3sxbdp0 ; _rtB -> p0fwkqizus =
0.0 ; _rtB -> p0fwkqizus += _rtP -> P_28 [ 0 ] * _rtX -> mjxmk3krb0 [ 0 ] ;
_rtB -> p0fwkqizus += _rtP -> P_28 [ 1 ] * _rtX -> mjxmk3krb0 [ 1 ] ; _rtB ->
p0fwkqizus += _rtP -> P_29 * _rtB -> apx33sizl1 ; _rtB -> lchfsfy0nh = 0.0 ;
_rtB -> lchfsfy0nh += _rtP -> P_31 * _rtX -> nlcoj2i5qm ; _rtB -> lchfsfy0nh
+= _rtP -> P_32 * _rtB -> p0fwkqizus ; UNUSED_PARAMETER ( tid ) ; }
#define MDL_UPDATE
static void mdlUpdate ( SimStruct * S , int_T tid ) { UNUSED_PARAMETER ( tid
) ; }
#define MDL_DERIVATIVES
static void mdlDerivatives ( SimStruct * S ) { htmb1f42yb * _rtB ; aa5zavtgxb
* _rtP ; bxkf2zvmyy * _rtX ; dnm5t4oa0t * _rtXdot ; _rtXdot = ( ( dnm5t4oa0t
* ) ssGetdX ( S ) ) ; _rtX = ( ( bxkf2zvmyy * ) ssGetContStates ( S ) ) ;
_rtP = ( ( aa5zavtgxb * ) ssGetDefaultParam ( S ) ) ; _rtB = ( ( htmb1f42yb *
) _ssGetBlockIO ( S ) ) ; _rtXdot -> nas0omrfkh [ 0 ] = 0.0 ; _rtXdot ->
nas0omrfkh [ 0 ] += _rtP -> P_0 [ 0 ] * _rtX -> nas0omrfkh [ 0 ] ; _rtXdot ->
nas0omrfkh [ 1 ] = 0.0 ; _rtXdot -> nas0omrfkh [ 0 ] += _rtP -> P_0 [ 1 ] *
_rtX -> nas0omrfkh [ 1 ] ; _rtXdot -> nas0omrfkh [ 1 ] += _rtX -> nas0omrfkh
[ 0 ] ; _rtXdot -> nas0omrfkh [ 0 ] += _rtB -> ek5nd0wwac ; _rtXdot ->
c53qp3dtca = _rtB -> mqjbxnvs0a ; _rtXdot -> peewifpgt1 = _rtB -> oqtkmx5vce
; _rtXdot -> hcymlbn1pk [ 0 ] = 0.0 ; _rtXdot -> hcymlbn1pk [ 0 ] += _rtP ->
P_9 [ 0 ] * _rtX -> hcymlbn1pk [ 0 ] ; _rtXdot -> hcymlbn1pk [ 1 ] = 0.0 ;
_rtXdot -> hcymlbn1pk [ 0 ] += _rtP -> P_9 [ 1 ] * _rtX -> hcymlbn1pk [ 1 ] ;
_rtXdot -> hcymlbn1pk [ 1 ] += _rtX -> hcymlbn1pk [ 0 ] ; _rtXdot ->
hcymlbn1pk [ 0 ] += _rtB -> ek5nd0wwac ; _rtXdot -> hakkqyygmj = _rtB ->
kkns3oxlmq ; _rtXdot -> aurwnltqa2 = _rtB -> fo12xfqqwn ; _rtXdot ->
p0mh0ay1l4 [ 0 ] = 0.0 ; _rtXdot -> p0mh0ay1l4 [ 0 ] += _rtP -> P_18 [ 0 ] *
_rtX -> p0mh0ay1l4 [ 0 ] ; _rtXdot -> p0mh0ay1l4 [ 1 ] = 0.0 ; _rtXdot ->
p0mh0ay1l4 [ 0 ] += _rtP -> P_18 [ 1 ] * _rtX -> p0mh0ay1l4 [ 1 ] ; _rtXdot
-> p0mh0ay1l4 [ 1 ] += _rtX -> p0mh0ay1l4 [ 0 ] ; _rtXdot -> p0mh0ay1l4 [ 0 ]
+= _rtB -> ik34kg002i ; _rtXdot -> gytq4zwpra [ 0 ] = 0.0 ; _rtXdot ->
gytq4zwpra [ 0 ] += _rtP -> P_21 [ 0 ] * _rtX -> gytq4zwpra [ 0 ] ; _rtXdot
-> gytq4zwpra [ 1 ] = 0.0 ; _rtXdot -> gytq4zwpra [ 0 ] += _rtP -> P_21 [ 1 ]
* _rtX -> gytq4zwpra [ 1 ] ; _rtXdot -> gytq4zwpra [ 1 ] += _rtX ->
gytq4zwpra [ 0 ] ; _rtXdot -> gytq4zwpra [ 0 ] += _rtB -> ik34kg002i ;
_rtXdot -> bjdkmyv0ro = _rtB -> mdedgzboxv ; _rtXdot -> psl3sxbdp0 = _rtB ->
lchfsfy0nh ; _rtXdot -> mjxmk3krb0 [ 0 ] = 0.0 ; _rtXdot -> mjxmk3krb0 [ 0 ]
+= _rtP -> P_27 [ 0 ] * _rtX -> mjxmk3krb0 [ 0 ] ; _rtXdot -> mjxmk3krb0 [ 1
] = 0.0 ; _rtXdot -> mjxmk3krb0 [ 0 ] += _rtP -> P_27 [ 1 ] * _rtX ->
mjxmk3krb0 [ 1 ] ; _rtXdot -> mjxmk3krb0 [ 1 ] += _rtX -> mjxmk3krb0 [ 0 ] ;
_rtXdot -> mjxmk3krb0 [ 0 ] += _rtB -> apx33sizl1 ; _rtXdot -> nlcoj2i5qm =
0.0 ; _rtXdot -> nlcoj2i5qm += _rtP -> P_30 * _rtX -> nlcoj2i5qm ; _rtXdot ->
nlcoj2i5qm += _rtB -> p0fwkqizus ; }
#define MDL_ZERO_CROSSINGS
static void mdlZeroCrossings ( SimStruct * S ) { aa5zavtgxb * _rtP ;
jz401ntygz * _rtZCSV ; _rtZCSV = ( ( jz401ntygz * ) ssGetSolverZcSignalVector
( S ) ) ; _rtP = ( ( aa5zavtgxb * ) ssGetDefaultParam ( S ) ) ; _rtZCSV ->
kgnqbqmwe1 = ssGetT ( S ) - _rtP -> P_4 ; _rtZCSV -> igwcasqsm4 = ssGetT ( S
) - _rtP -> P_14 ; } static void mdlInitializeSizes ( SimStruct * S ) {
ssSetChecksumVal ( S , 0 , 3639000206U ) ; ssSetChecksumVal ( S , 1 ,
256501934U ) ; ssSetChecksumVal ( S , 2 , 2000498432U ) ; ssSetChecksumVal (
S , 3 , 2382711419U ) ; { mxArray * slVerStructMat = NULL ; mxArray *
slStrMat = mxCreateString ( "simulink" ) ; char slVerChar [ 10 ] ; int status
= mexCallMATLAB ( 1 , & slVerStructMat , 1 , & slStrMat , "ver" ) ; if (
status == 0 ) { mxArray * slVerMat = mxGetField ( slVerStructMat , 0 ,
"Version" ) ; if ( slVerMat == NULL ) { status = 1 ; } else { status =
mxGetString ( slVerMat , slVerChar , 10 ) ; } } mxDestroyArray ( slStrMat ) ;
mxDestroyArray ( slVerStructMat ) ; if ( ( status == 1 ) || ( strcmp (
slVerChar , "8.6" ) != 0 ) ) { return ; } } ssSetOptions ( S ,
SS_OPTION_EXCEPTION_FREE_CODE ) ; if ( ssGetSizeofDWork ( S ) != sizeof (
mpt0mzz342 ) ) { ssSetErrorStatus ( S ,
"Unexpected error: Internal DWork sizes do "
"not match for accelerator mex file." ) ; } if ( ssGetSizeofGlobalBlockIO ( S
) != sizeof ( htmb1f42yb ) ) { ssSetErrorStatus ( S ,
"Unexpected error: Internal BlockIO sizes do "
"not match for accelerator mex file." ) ; } { int ssSizeofParams ;
ssGetSizeofParams ( S , & ssSizeofParams ) ; if ( ssSizeofParams != sizeof (
aa5zavtgxb ) ) { static char msg [ 256 ] ; sprintf ( msg ,
"Unexpected error: Internal Parameters sizes do "
"not match for accelerator mex file." ) ; } } _ssSetDefaultParam ( S , (
real_T * ) & h1o4dzbgiy ) ; } static void mdlInitializeSampleTimes (
SimStruct * S ) { } static void mdlTerminate ( SimStruct * S ) { }
#include "simulink.c"
