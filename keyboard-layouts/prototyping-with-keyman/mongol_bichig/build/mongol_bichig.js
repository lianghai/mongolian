if(typeof keyman === 'undefined') {
  console.log('Keyboard requires KeymanWeb 10.0 or later');
  if(typeof tavultesoft !== 'undefined') tavultesoft.keymanweb.util.alert("This keyboard requires KeymanWeb 10.0 or later");
} else {
KeymanWeb.KR(new Keyboard_mongol_bichig());
}
function Keyboard_mongol_bichig()
{
  var modCodes = keyman.osk.modifierCodes;
  var keyCodes = keyman.osk.keyCodes;

  this.KI="Keyboard_mongol_bichig";
  this.KN="Mongol Bichig";
  this.KMINVER="10.0";
  this.KV={F:' 1em "Noto Sans Mongolian"',K102:0};
  this.KV.KLS={
    "default": ["=","№","-","\"","₮",":",".","_",",","%","?","","","","","","ᠹ","ᠼ","ᠤ⁵","ᠵ","ᠡ","ᠨ","ᠭ","ᠱ","ᠦ⁷","ᠽ","ᠻ","᠊","\\","","","","ᠶ","","ᠪ","ᠥ⁶","ᠠ","ᠬ","ᠷ","ᠣ⁴","ᠯ","ᠳ","ᠫ","","","","","","","","ᠴ","","ᠰ","ᠮ","ᠢ","ᠲ","","ᠸ","↹","","","","","",""],
    "shift": ["+","1","2","3","4","5","6","7","8","9","0","","","","","","","","","ᠿ","ᠧ","","","","","","","᠇","|","","","","","","","","","ᠾ","","","","","","","","","","","","","","","","","","","","","","","","","",""," "]
  };
  this.KV.BK=(function(x){
    var
      empty=Array.apply(null, Array(65)).map(String.prototype.valueOf,""),
      result=[], v, i,
      modifiers=['default','shift','ctrl','shift-ctrl','alt','shift-alt','ctrl-alt','shift-ctrl-alt'];
    for(i=modifiers.length-1;i>=0;i--) {
      v = x[modifiers[i]];
      if(v || result.length > 0) {
        result=(v ? v : empty).slice().concat(result);
      }
    }
    return result;
  })(this.KV.KLS);
  this.KDU=0;
  this.KH='';
  this.KM=0;
  this.KBVER="0.1";
  this.KMBM=modCodes.SHIFT /* 0x0010 */;
  this.KVKL={
  "tablet": {
    "displayUnderlying": false,
    "layer": [
      {
        "id": "default",
        "row": [
          {
            "id": "1",
            "key": [
              {
                "id": "K_1",
                "text": "\u2116"
              },
              {
                "id": "K_2",
                "text": "-"
              },
              {
                "id": "K_3",
                "text": "\""
              },
              {
                "id": "K_4",
                "text": "\u20AE"
              },
              {
                "id": "K_5",
                "text": ":"
              },
              {
                "id": "K_6",
                "text": "."
              },
              {
                "id": "K_7",
                "text": "_"
              },
              {
                "id": "K_8",
                "text": ","
              },
              {
                "id": "K_9",
                "text": "%"
              },
              {
                "id": "K_0",
                "text": "?"
              },
              {
                "id": "K_HYPHEN",
                "text": "\u0435"
              },
              {
                "id": "K_EQUAL",
                "text": "\u0449"
              },
              {
                "width": "100",
                "id": "K_BKSP",
                "sp": "1",
                "text": "*BkSp*"
              }
            ]
          },
          {
            "id": "2",
            "key": [
              {
                "id": "K_Q",
                "pad": "75",
                "text": "\u0444"
              },
              {
                "id": "K_W",
                "text": "\u0446"
              },
              {
                "id": "K_E",
                "text": "\u0443"
              },
              {
                "id": "K_R",
                "text": "\u0436"
              },
              {
                "id": "K_T",
                "text": "\u044D"
              },
              {
                "id": "K_Y",
                "text": "\u043D"
              },
              {
                "id": "K_U",
                "text": "\u0433"
              },
              {
                "id": "K_I",
                "text": "\u0448"
              },
              {
                "id": "K_O",
                "text": "\u04AF"
              },
              {
                "id": "K_P",
                "text": "\u0437"
              },
              {
                "id": "K_LBRKT",
                "text": "\u043A"
              },
              {
                "id": "K_RBRKT",
                "text": "\u044A"
              },
              {
                "width": "10",
                "sp": "10"
              }
            ]
          },
          {
            "id": "3",
            "key": [
              {
                "id": "K_BKQUOTE",
                "text": "="
              },
              {
                "id": "K_A",
                "text": "\u0439"
              },
              {
                "id": "K_S",
                "text": "\u044B"
              },
              {
                "id": "K_D",
                "text": "\u0431"
              },
              {
                "id": "K_F",
                "text": "\u04E9"
              },
              {
                "id": "K_G",
                "text": "\u0430"
              },
              {
                "id": "K_H",
                "text": "\u0445"
              },
              {
                "id": "K_J",
                "text": "\u0440"
              },
              {
                "id": "K_K",
                "text": "\u043E"
              },
              {
                "id": "K_L",
                "text": "\u043B"
              },
              {
                "id": "K_COLON",
                "text": "\u0434"
              },
              {
                "id": "K_QUOTE",
                "text": "\u043F"
              },
              {
                "id": "K_BKSLASH",
                "text": "\\"
              }
            ]
          },
          {
            "id": "4",
            "key": [
              {
                "width": "160",
                "id": "K_SHIFT",
                "sp": "1",
                "text": "*Shift*"
              },
              {
                "id": "K_oE2",
                "text": "\\"
              },
              {
                "id": "K_Z",
                "text": "\u044F"
              },
              {
                "id": "K_X",
                "text": "\u0447"
              },
              {
                "id": "K_C",
                "text": "\u0451"
              },
              {
                "id": "K_V",
                "text": "\u0441"
              },
              {
                "id": "K_B",
                "text": "\u043C"
              },
              {
                "id": "K_N",
                "text": "\u0438"
              },
              {
                "id": "K_M",
                "text": "\u0442"
              },
              {
                "id": "K_COMMA",
                "text": "\u044C"
              },
              {
                "id": "K_PERIOD",
                "text": "\u0432"
              },
              {
                "id": "K_SLASH",
                "text": "\u044E"
              },
              {
                "width": "10",
                "sp": "10"
              }
            ]
          },
          {
            "id": "5",
            "key": [
              {
                "nextlayer": "ctrl",
                "width": "130",
                "id": "K_LCONTROL",
                "sp": "1",
                "text": "ctrl"
              },
              {
                "width": "140",
                "id": "K_LOPT",
                "sp": "1",
                "text": "*Menu*"
              },
              {
                "width": "930",
                "id": "K_SPACE"
              },
              {
                "width": "145",
                "id": "K_ENTER",
                "sp": "1",
                "text": "*Enter*"
              }
            ]
          }
        ]
      },
      {
        "id": "shift",
        "row": [
          {
            "id": "1",
            "key": [
              {
                "id": "K_1",
                "text": "1"
              },
              {
                "id": "K_2",
                "text": "2"
              },
              {
                "id": "K_3",
                "text": "3"
              },
              {
                "id": "K_4",
                "text": "4"
              },
              {
                "id": "K_5",
                "text": "5"
              },
              {
                "id": "K_6",
                "text": "6"
              },
              {
                "id": "K_7",
                "text": "7"
              },
              {
                "id": "K_8",
                "text": "8"
              },
              {
                "id": "K_9",
                "text": "9"
              },
              {
                "id": "K_0",
                "text": "0"
              },
              {
                "id": "K_HYPHEN",
                "text": "\u0415"
              },
              {
                "id": "K_EQUAL",
                "text": "\u0429"
              },
              {
                "width": "100",
                "id": "K_BKSP",
                "sp": "1",
                "text": "*BkSp*"
              }
            ]
          },
          {
            "id": "2",
            "key": [
              {
                "id": "K_Q",
                "pad": "75",
                "text": "\u0424"
              },
              {
                "id": "K_W",
                "text": "\u0426"
              },
              {
                "id": "K_E",
                "text": "\u0423"
              },
              {
                "id": "K_R",
                "text": "\u0416"
              },
              {
                "id": "K_T",
                "text": "\u042D"
              },
              {
                "id": "K_Y",
                "text": "\u041D"
              },
              {
                "id": "K_U",
                "text": "\u0413"
              },
              {
                "id": "K_I",
                "text": "\u0428"
              },
              {
                "id": "K_O",
                "text": "\u04AE"
              },
              {
                "id": "K_P",
                "text": "\u0417"
              },
              {
                "id": "K_LBRKT",
                "text": "\u041A"
              },
              {
                "id": "K_RBRKT",
                "text": "\u042A"
              },
              {
                "width": "10",
                "sp": "10"
              }
            ]
          },
          {
            "id": "3",
            "key": [
              {
                "id": "K_BKQUOTE",
                "text": "+"
              },
              {
                "id": "K_A",
                "text": "\u0419"
              },
              {
                "id": "K_S",
                "text": "\u042B"
              },
              {
                "id": "K_D",
                "text": "\u0411"
              },
              {
                "id": "K_F",
                "text": "\u04E8"
              },
              {
                "id": "K_G",
                "text": "\u0410"
              },
              {
                "id": "K_H",
                "text": "\u0425"
              },
              {
                "id": "K_J",
                "text": "\u0420"
              },
              {
                "id": "K_K",
                "text": "\u041E"
              },
              {
                "id": "K_L",
                "text": "\u041B"
              },
              {
                "id": "K_COLON",
                "text": "\u0414"
              },
              {
                "id": "K_QUOTE",
                "text": "\u041F"
              },
              {
                "id": "K_BKSLASH",
                "text": "|"
              }
            ]
          },
          {
            "id": "4",
            "key": [
              {
                "width": "160",
                "id": "K_SHIFT",
                "sp": "1",
                "text": "*Shift*"
              },
              {
                "id": "K_oE2",
                "text": "|"
              },
              {
                "id": "K_Z",
                "text": "\u042F"
              },
              {
                "id": "K_X",
                "text": "\u0427"
              },
              {
                "id": "K_C",
                "text": "\u0401"
              },
              {
                "id": "K_V",
                "text": "\u0421"
              },
              {
                "id": "K_B",
                "text": "\u041C"
              },
              {
                "id": "K_N",
                "text": "\u0418"
              },
              {
                "id": "K_M",
                "text": "\u0422"
              },
              {
                "id": "K_COMMA",
                "text": "\u042C"
              },
              {
                "id": "K_PERIOD",
                "text": "\u0412"
              },
              {
                "id": "K_SLASH",
                "text": "\u042E"
              },
              {
                "width": "10",
                "sp": "10"
              }
            ]
          },
          {
            "id": "5",
            "key": [
              {
                "nextlayer": "ctrl",
                "width": "130",
                "id": "K_LCONTROL",
                "sp": "1",
                "text": "ctrl"
              },
              {
                "width": "140",
                "id": "K_LOPT",
                "sp": "1",
                "text": "*Menu*"
              },
              {
                "width": "930",
                "id": "K_SPACE"
              },
              {
                "width": "145",
                "id": "K_ENTER",
                "sp": "1",
                "text": "*Enter*"
              }
            ]
          }
        ]
      },
      {
        "id": "ctrl",
        "row": [
          {
            "id": "1",
            "key": [
              {
                "id": "K_1"
              },
              {
                "id": "K_2"
              },
              {
                "id": "K_3"
              },
              {
                "id": "K_4"
              },
              {
                "id": "K_5"
              },
              {
                "id": "K_6"
              },
              {
                "id": "K_7"
              },
              {
                "id": "K_8"
              },
              {
                "id": "K_9"
              },
              {
                "id": "K_0"
              },
              {
                "id": "K_HYPHEN"
              },
              {
                "id": "K_EQUAL"
              },
              {
                "width": "100",
                "id": "K_BKSP",
                "sp": "1",
                "text": "*BkSp*"
              }
            ]
          },
          {
            "id": "2",
            "key": [
              {
                "id": "K_Q",
                "pad": "75"
              },
              {
                "id": "K_W"
              },
              {
                "id": "K_E"
              },
              {
                "id": "K_R"
              },
              {
                "id": "K_T"
              },
              {
                "id": "K_Y"
              },
              {
                "id": "K_U"
              },
              {
                "id": "K_I"
              },
              {
                "id": "K_O"
              },
              {
                "id": "K_P"
              },
              {
                "id": "K_LBRKT"
              },
              {
                "id": "K_RBRKT"
              },
              {
                "width": "10",
                "sp": "10"
              }
            ]
          },
          {
            "id": "3",
            "key": [
              {
                "id": "K_BKQUOTE"
              },
              {
                "id": "K_A"
              },
              {
                "id": "K_S"
              },
              {
                "id": "K_D"
              },
              {
                "id": "K_F"
              },
              {
                "id": "K_G"
              },
              {
                "id": "K_H"
              },
              {
                "id": "K_J"
              },
              {
                "id": "K_K"
              },
              {
                "id": "K_L"
              },
              {
                "id": "K_COLON"
              },
              {
                "id": "K_QUOTE"
              },
              {
                "id": "K_BKSLASH"
              }
            ]
          },
          {
            "id": "4",
            "key": [
              {
                "width": "160",
                "id": "K_SHIFT",
                "sp": "1",
                "text": "*Shift*"
              },
              {
                "id": "K_oE2"
              },
              {
                "id": "K_Z"
              },
              {
                "id": "K_X"
              },
              {
                "id": "K_C"
              },
              {
                "id": "K_V"
              },
              {
                "id": "K_B"
              },
              {
                "id": "K_N"
              },
              {
                "id": "K_M"
              },
              {
                "id": "K_COMMA"
              },
              {
                "id": "K_PERIOD"
              },
              {
                "id": "K_SLASH"
              },
              {
                "width": "10",
                "sp": "10"
              }
            ]
          },
          {
            "id": "5",
            "key": [
              {
                "nextlayer": "default",
                "width": "130",
                "id": "K_LCONTROL",
                "sp": "1",
                "text": "default"
              },
              {
                "width": "140",
                "id": "K_LOPT",
                "sp": "1",
                "text": "*Menu*"
              },
              {
                "width": "930",
                "id": "K_SPACE"
              },
              {
                "width": "145",
                "id": "K_ENTER",
                "sp": "1",
                "text": "*Enter*"
              }
            ]
          }
        ]
      }
    ]
  }
}
;
  this.s_o="ᠣ";
  this.s_u="ᠤ";
  this.s_oe="ᠥ";
  this.s_ue="ᠦ";
  this.s_aleph="᠇";
  this.s_nirugu="᠊";
  this.s_MVS="᠎";
  this.s_NNBSP=" ";
  this.s_FVS1="᠋";
  this.s_FVS2="᠌";
  this.s_FVS3="᠍";
  this.s_vowel_masculine="ᠠᠣᠤ";
  this.s_vowel_feminine="ᠡᠧᠥᠦ";
  this.s_vowel_neuter="ᠢ";
  this.s_vowel="ᠠᠣᠤᠡᠧᠥᠦᠢ";
  this.s_consonant="ᠨᠩᠪᠫᠬᠭᠮᠯᠰᠱᠲᠳᠴᠵᠶᠷᠸᠹᠻᠼᠽᠾᠿᡀᡁᡂ᠇";
  this.s_letter="ᠠᠣᠤᠡᠧᠥᠦᠢᠨᠩᠪᠫᠬᠭᠮᠯᠰᠱᠲᠳᠴᠵᠶᠷᠸᠹᠻᠼᠽᠾᠿᡀᡁᡂ᠇";
  this.s_letter_key=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''];
  this.s_letter_key_output="ᠹᠼᠤᠵᠿᠡᠧᠨᠭᠱᠦᠽᠻ᠇ᠶᠪᠥᠠᠬᠾᠷᠣᠯᠳᠫᠴᠰᠮᠢᠲᠸ";
  this.s_nirugu_key=[''];
  this.s_next=[''];
  this.s_vowel_4567="ᠣᠤᠥᠦ";
  this.s_vowel_12="ᠠᠡ";
  this.s_consonant_h_g="ᠬᠭ";
  this.s_consonant_n_m_l_y_r_w="ᠨᠮᠯᠶᠷᠸ";
  this.KVER="13.0.101.0";
  this.gs=function(t,e) {
    return this.g_main(t,e);
  };
  this.g_main=function(t,e) {
    var k=KeymanWeb,r=0,m=0;
    if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_BKSP /* 0x08 */)) {
      if(k.KFCM(3,t,[{t:'a',a:this.s_consonant_h_g},'ᠠ','᠊'])){
        r=m=1;   // Line 295
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant_h_g,1,t);
        k.KO(-1,t,"᠎");
        k.KO(-1,t,"ᠠ");
      }
      else if(k.KFCM(3,t,[{t:'a',a:this.s_consonant_n_m_l_y_r_w},{t:'a',a:this.s_vowel_12},'᠊'])){
        r=m=1;   // Line 296
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant_n_m_l_y_r_w,1,t);
        k.KO(-1,t,"᠎");
        k.KIO(-1,this.s_vowel_12,2,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_SPACE /* 0x20 */)) {
      if(1){
        r=m=1;   // Line 220
        k.KDC(0,t);
        k.KO(-1,t," ");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_SPACE /* 0x20 */)) {
      if(1){
        r=m=1;   // Line 221
        k.KDC(0,t);
        k.KO(-1,t," ");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_1 /* 0x31 */)) {
      if(1){
        r=m=1;   // Line 91
        k.KDC(0,t);
        k.KO(-1,t,"1");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_3 /* 0x33 */)) {
      if(1){
        r=m=1;   // Line 97
        k.KDC(0,t);
        k.KO(-1,t,"3");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_4 /* 0x34 */)) {
      if(1){
        r=m=1;   // Line 100
        k.KDC(0,t);
        k.KO(-1,t,"4");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_5 /* 0x35 */)) {
      if(1){
        r=m=1;   // Line 103
        k.KDC(0,t);
        k.KO(-1,t,"5");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_7 /* 0x37 */)) {
      if(1){
        r=m=1;   // Line 109
        k.KDC(0,t);
        k.KO(-1,t,"7");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_QUOTE /* 0xDE */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠫ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠫ᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_9 /* 0x39 */)) {
      if(1){
        r=m=1;   // Line 115
        k.KDC(0,t);
        k.KO(-1,t,"9");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_0 /* 0x30 */)) {
      if(1){
        r=m=1;   // Line 118
        k.KDC(0,t);
        k.KO(-1,t,"0");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_8 /* 0x38 */)) {
      if(1){
        r=m=1;   // Line 112
        k.KDC(0,t);
        k.KO(-1,t,"8");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_EQUAL /* 0xBB */)) {
      if(1){
        r=m=1;   // Line 124
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_COMMA /* 0xBC */)) {
      if(1){
        r=m=1;   // Line 209
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_HYPHEN /* 0xBD */)) {
      if(1){
        r=m=1;   // Line 120
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_PERIOD /* 0xBE */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠸ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠸ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_SLASH /* 0xBF */)) {
      if(k.KFCM(4,t,['ᠢ','ᠭ','᠋','᠊'])){
        r=m=1;   // Line 249
        k.KDC(4,t);
        k.KO(-1,t,"ᠢ");
        k.KO(-1,t,"ᠭ");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(4,t,['ᠲ','᠋',{t:'a',a:this.s_vowel},'᠊'])){
        r=m=1;   // Line 267
        k.KDC(4,t);
        k.KO(-1,t,"ᠲ");
        k.KIO(-1,this.s_vowel,3,t);
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(4,t,['ᠳ','᠋',{t:'a',a:this.s_vowel},'᠊'])){
        r=m=1;   // Line 274
        k.KDC(4,t);
        k.KO(-1,t,"ᠳ");
        k.KIO(-1,this.s_vowel,3,t);
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(3,t,['ᠳ','᠋','᠊'])){
        r=m=1;   // Line 242
        k.KDC(3,t);
        k.KO(-1,t,"ᠳ");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(3,t,['ᠢ','ᠭ','᠊'])){
        r=m=1;   // Line 247
        k.KDC(3,t);
        k.KO(-1,t,"ᠢ");
        k.KO(-1,t,"ᠭ᠋");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(3,t,['ᠢ','ᠭ','᠋'])){
        r=m=1;   // Line 248
        k.KDC(3,t);
        k.KO(-1,t,"ᠢ");
        k.KO(-1,t,"ᠭ");
      }
      else if(k.KFCM(3,t,['ᠲ',{t:'a',a:this.s_vowel},'᠊'])){
        r=m=1;   // Line 265
        k.KDC(3,t);
        k.KO(-1,t,"ᠲ᠋");
        k.KIO(-1,this.s_vowel,2,t);
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(3,t,['ᠲ','᠋',{t:'a',a:this.s_vowel}])){
        r=m=1;   // Line 266
        k.KDC(3,t);
        k.KO(-1,t,"ᠲ");
        k.KIO(-1,this.s_vowel,3,t);
      }
      else if(k.KFCM(3,t,['ᠳ',{t:'a',a:this.s_vowel},'᠊'])){
        r=m=1;   // Line 272
        k.KDC(3,t);
        k.KO(-1,t,"ᠳ᠋");
        k.KIO(-1,this.s_vowel,2,t);
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(3,t,['ᠳ','᠋',{t:'a',a:this.s_vowel}])){
        r=m=1;   // Line 273
        k.KDC(3,t);
        k.KO(-1,t,"ᠳ");
        k.KIO(-1,this.s_vowel,3,t);
      }
      else if(k.KFCM(3,t,[{t:'a',a:this.s_consonant},{t:'a',a:this.s_vowel_4567},'᠋'])){
        r=m=1;   // Line 281
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant,1,t);
        k.KIO(-1,this.s_vowel_4567,2,t);
      }
      else if(k.KFCM(3,t,[{t:'a',a:this.s_consonant_h_g},'᠎','ᠠ'])){
        r=m=1;   // Line 299
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant_h_g,1,t);
        k.KO(-1,t,"ᠠ");
      }
      else if(k.KFCM(3,t,[{t:'a',a:this.s_consonant_n_m_l_y_r_w},'᠎',{t:'a',a:this.s_vowel_12}])){
        r=m=1;   // Line 301
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant_n_m_l_y_r_w,1,t);
        k.KIO(-1,this.s_vowel_12,3,t);
      }
      else if(k.KFCM(2,t,['ᠨ','᠊'])){
        r=m=1;   // Line 235
        k.KDC(2,t);
        k.KO(-1,t,"ᠩ");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(2,t,['ᠩ','᠊'])){
        r=m=1;   // Line 237
        k.KDC(2,t);
        k.KO(-1,t,"ᠨ");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(2,t,['ᠳ','᠊'])){
        r=m=1;   // Line 240
        k.KDC(2,t);
        k.KO(-1,t,"ᠳ᠋");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(2,t,['ᠳ','᠋'])){
        r=m=1;   // Line 241
        k.KDC(2,t);
        k.KO(-1,t,"ᠳ");
      }
      else if(k.KFCM(2,t,['ᠢ','ᠭ'])){
        r=m=1;   // Line 246
        k.KDC(2,t);
        k.KO(-1,t,"ᠢ");
        k.KO(-1,t,"ᠭ᠋");
      }
      else if(k.KFCM(2,t,['ᠠ','᠋'])){
        r=m=1;   // Line 257
        k.KDC(2,t);
        k.KO(-1,t,"ᠠ");
      }
      else if(k.KFCM(2,t,['ᠦ','᠋'])){
        r=m=1;   // Line 260
        k.KDC(2,t);
        k.KO(-1,t,"ᠦ");
      }
      else if(k.KFCM(2,t,['ᠲ',{t:'a',a:this.s_vowel}])){
        r=m=1;   // Line 264
        k.KDC(2,t);
        k.KO(-1,t,"ᠲ᠋");
        k.KIO(-1,this.s_vowel,2,t);
      }
      else if(k.KFCM(2,t,['ᠳ',{t:'a',a:this.s_vowel}])){
        r=m=1;   // Line 271
        k.KDC(2,t);
        k.KO(-1,t,"ᠳ᠋");
        k.KIO(-1,this.s_vowel,2,t);
      }
      else if(k.KFCM(2,t,[{t:'a',a:this.s_consonant},{t:'a',a:this.s_vowel_4567}])){
        r=m=1;   // Line 280
        k.KDC(2,t);
        k.KIO(-1,this.s_consonant,1,t);
        k.KIO(-1,this.s_vowel_4567,2,t);
        k.KO(-1,t,"᠋");
      }
      else if(k.KFCM(2,t,[{t:'a',a:this.s_consonant_h_g},'ᠠ'])){
        r=m=1;   // Line 298
        k.KDC(2,t);
        k.KIO(-1,this.s_consonant_h_g,1,t);
        k.KO(-1,t,"᠎");
        k.KO(-1,t,"ᠠ");
      }
      else if(k.KFCM(2,t,[{t:'a',a:this.s_consonant_n_m_l_y_r_w},{t:'a',a:this.s_vowel_12}])){
        r=m=1;   // Line 300
        k.KDC(2,t);
        k.KIO(-1,this.s_consonant_n_m_l_y_r_w,1,t);
        k.KO(-1,t,"᠎");
        k.KIO(-1,this.s_vowel_12,2,t);
      }
      else if(k.KFCM(2,t,['ᠵ','ᠢ'])){
        r=m=1;   // Line 310
        k.KDC(2,t);
        k.KO(-1,t,"ᡁ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᡁ','ᠢ'])){
        r=m=1;   // Line 311
        k.KDC(2,t);
        k.KO(-1,t,"ᠵ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᠴ','ᠢ'])){
        r=m=1;   // Line 313
        k.KDC(2,t);
        k.KO(-1,t,"ᡂ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᡂ','ᠢ'])){
        r=m=1;   // Line 314
        k.KDC(2,t);
        k.KO(-1,t,"ᠴ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᠰ','ᠢ'])){
        r=m=1;   // Line 316
        k.KDC(2,t);
        k.KO(-1,t,"ᠱ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᠱ','ᠢ'])){
        r=m=1;   // Line 317
        k.KDC(2,t);
        k.KO(-1,t,"ᠰ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᠷ','ᠢ'])){
        r=m=1;   // Line 319
        k.KDC(2,t);
        k.KO(-1,t,"ᠿ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(2,t,['ᠿ','ᠢ'])){
        r=m=1;   // Line 320
        k.KDC(2,t);
        k.KO(-1,t,"ᠷ");
        k.KO(-1,t,"ᠢ");
      }
      else if(k.KFCM(1,t,['ᠨ'])){
        r=m=1;   // Line 234
        k.KDC(1,t);
        k.KO(-1,t,"ᠩ");
      }
      else if(k.KFCM(1,t,['ᠩ'])){
        r=m=1;   // Line 236
        k.KDC(1,t);
        k.KO(-1,t,"ᠨ");
      }
      else if(k.KFCM(1,t,['ᠳ'])){
        r=m=1;   // Line 239
        k.KDC(1,t);
        k.KO(-1,t,"ᠳ᠋");
      }
      else if(k.KFCM(1,t,['ᠠ'])){
        r=m=1;   // Line 256
        k.KDC(1,t);
        k.KO(-1,t,"ᠠ᠋");
      }
      else if(k.KFCM(1,t,['ᠦ'])){
        r=m=1;   // Line 259
        k.KDC(1,t);
        k.KO(-1,t,"ᠦ᠋");
      }
      else if(1){
        r=m=1;   // Line 214
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_0 /* 0x30 */)) {
      if(1){
        r=m=1;   // Line 117
        k.KDC(0,t);
        k.KO(-1,t,"?");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_1 /* 0x31 */)) {
      if(1){
        r=m=1;   // Line 90
        k.KDC(0,t);
        k.KO(-1,t,"№");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_2 /* 0x32 */)) {
      if(1){
        r=m=1;   // Line 93
        k.KDC(0,t);
        k.KO(-1,t,"-");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_3 /* 0x33 */)) {
      if(1){
        r=m=1;   // Line 96
        k.KDC(0,t);
        k.KO(-1,t,"\"");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_4 /* 0x34 */)) {
      if(1){
        r=m=1;   // Line 99
        k.KDC(0,t);
        k.KO(-1,t,"₮");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_5 /* 0x35 */)) {
      if(1){
        r=m=1;   // Line 102
        k.KDC(0,t);
        k.KO(-1,t,":");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_6 /* 0x36 */)) {
      if(1){
        r=m=1;   // Line 105
        k.KDC(0,t);
        k.KO(-1,t,".");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_7 /* 0x37 */)) {
      if(1){
        r=m=1;   // Line 108
        k.KDC(0,t);
        k.KO(-1,t,"_");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_8 /* 0x38 */)) {
      if(1){
        r=m=1;   // Line 111
        k.KDC(0,t);
        k.KO(-1,t,",");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_9 /* 0x39 */)) {
      if(1){
        r=m=1;   // Line 114
        k.KDC(0,t);
        k.KO(-1,t,"%");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_COLON /* 0xBA */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠳ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠳ᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_COMMA /* 0xBC */)) {
      if(1){
        r=m=1;   // Line 210
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_EQUAL /* 0xBB */)) {
      if(1){
        r=m=1;   // Line 123
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_SLASH /* 0xBF */)) {
      if(1){
        r=m=1;   // Line 215
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_2 /* 0x32 */)) {
      if(1){
        r=m=1;   // Line 94
        k.KDC(0,t);
        k.KO(-1,t,"2");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_C /* 0x43 */)) {
      if(1){
        r=m=1;   // Line 199
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_H /* 0x48 */)) {
      if(k.KFCM(2,t,['ᠯ','᠊'])){
        r=m=1;   // Line 77
        k.KDC(2,t);
        k.KO(-1,t,"ᡀ");
        k.KO(-1,t,"᠊");
      }
      else if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠾ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠾ᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_R /* 0x52 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠿ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠿ᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_S /* 0x53 */)) {
      if(1){
        r=m=1;   // Line 168
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_T /* 0x54 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠧ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠧ᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_Z /* 0x5A */)) {
      if(1){
        r=m=1;   // Line 194
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_LBRKT /* 0xDB */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠻ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠻ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_BKSLASH /* 0xDC */)) {
      if(1){
        r=m=1;   // Line 159
        k.KDC(0,t);
        k.KO(-1,t,"\\");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_RBRKT /* 0xDD */)) {
      if(k.KFCM(3,t,[{t:'a',a:this.s_consonant_h_g},'᠎','ᠠ'])){
        r=m=1;   // Line 303
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant_h_g,1,t);
        k.KO(-1,t,"ᠠ᠊");
      }
      else if(k.KFCM(3,t,[{t:'a',a:this.s_consonant_n_m_l_y_r_w},'᠎',{t:'a',a:this.s_vowel_12}])){
        r=m=1;   // Line 304
        k.KDC(3,t);
        k.KIO(-1,this.s_consonant_n_m_l_y_r_w,1,t);
        k.KIO(-1,this.s_vowel_12,3,t);
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 156
        k.KDC(0,t);
        k.KO(-1,t,"᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_6 /* 0x36 */)) {
      if(1){
        r=m=1;   // Line 106
        k.KDC(0,t);
        k.KO(-1,t,"6");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_HYPHEN /* 0xBD */)) {
      if(1){
        r=m=1;   // Line 121
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_BKQUOTE /* 0xC0 */)) {
      if(1){
        r=m=1;   // Line 87
        k.KDC(0,t);
        k.KO(-1,t,"=");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_A /* 0x41 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠶ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠶ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_B /* 0x42 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠮ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠮ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_C /* 0x43 */)) {
      if(1){
        r=m=1;   // Line 198
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_D /* 0x44 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠪ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠪ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_E /* 0x45 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠤ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠤ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_F /* 0x46 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠥ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠥ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_G /* 0x47 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠠ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠠ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_H /* 0x48 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠬ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠬ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_I /* 0x49 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠱ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠱ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_J /* 0x4A */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠷ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠷ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_K /* 0x4B */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠣ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠣ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_L /* 0x4C */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠯ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠯ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_M /* 0x4D */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠲ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠲ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_N /* 0x4E */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠢ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠢ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_O /* 0x4F */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠦ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠦ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_P /* 0x50 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠽ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠽ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_Q /* 0x51 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠹ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠹ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_R /* 0x52 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠵ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠵ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_S /* 0x53 */)) {
      if(1){
        r=m=1;   // Line 167
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_T /* 0x54 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠡ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠡ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_U /* 0x55 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠭ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠭ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_V /* 0x56 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠰ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠰ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_W /* 0x57 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠼ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠼ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_X /* 0x58 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠴ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠴ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_Y /* 0x59 */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"ᠨ");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"ᠨ᠊");
      }
    }
    else if(k.KKM(e, modCodes.VIRTUAL_KEY /* 0x4000 */, keyCodes.K_Z /* 0x5A */)) {
      if(1){
        r=m=1;   // Line 193
        k.KDC(0,t);
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_BKSLASH /* 0xDC */)) {
      if(1){
        r=m=1;   // Line 160
        k.KDC(0,t);
        k.KO(-1,t,"|");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_RBRKT /* 0xDD */)) {
      if(k.KFCM(2,t,[{t:'a',a:this.s_letter},'᠊'])){
        r=m=1;   // Line 81
        k.KDC(2,t);
        k.KIO(-1,this.s_letter,1,t);
        k.KO(-1,t,"᠇");
        k.KO(-1,t,"᠊");
      }
      else if(1){
        r=m=1;   // Line 82
        k.KDC(0,t);
        k.KO(-1,t,"᠇᠊");
      }
    }
    else if(k.KKM(e, modCodes.SHIFT | modCodes.VIRTUAL_KEY /* 0x4010 */, keyCodes.K_BKQUOTE /* 0xC0 */)) {
      if(1){
        r=m=1;   // Line 88
        k.KDC(0,t);
        k.KO(-1,t,"+");
      }
    }
    return r;
  };
}
