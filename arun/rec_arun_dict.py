#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Arun data sets.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Dinc/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {1: {"0001": 641.6}, 2: {"0002": 641.6}, 3: {"0003": 641.6}, 4: {"0004": 641.6}, 5: {"0005": 641.6}, 6: {"0006": 641.6}, 7: {"0007": 648.0}, 8: {"0008": 644.5}, 9: {"0009": 645.5}, 10: {"0010": 644.0},  
    11: {"0011": 644.5}, 12: {"0012": 648.0}, 13: {"0013": 648.0}, 14: {"0014": 647.3}, 15: {"0015": 647.5}, 16: {"0016": 648.0}, 17: {"0017": 648.5}, 18: {"0018": 646.5}, 19: {"0019": 648.0}, 20: {"0020": 648.3}, 
    21: {"0021": 648.4}, 22: {"0022": 648.5}, 23: {"0023": 648.5}, 24: {"0024": 648.5}, 25: {"0025": 648.5}, 26: {"0026": 648.5}, 27: {"0027": 648.5}, 28: {"0028": 648.5}, 29: {"0029": 648.5}, 30: {"0030": 648.5}, 
    31: {"0031": 648.5}, 32: {"0032": 648.5}, 33: {"0033": 648.5}, 34: {"0034": 648.5}, 35: {"0035": 648.5}, 36: {"0036": 648.5}, 37: {"0037": 648.5}, 38: {"0038": 648.5}, 39: {"0039": 648.5}, 40: {"0040": 648.5}, 
    41: {"0041": 648.5}, 42: {"0042": 648.5}, 43: {"0043": 648.5}, 44: {"0044": 648.5}, 45: {"0045": 648.5}, 46: {"0046": 648.5}, 47: {"0047": 648.5}, 48: {"0048": 648.5}, 49: {"0049": 648.5}, 50: {"0050": 648.5}, 
    51: {"0051": 648.5}, 52: {"0052": 648.5}, 53: {"0053": 648.5}, 54: {"0054": 648.5}, 55: {"0055": 648.5}, 56: {"0056": 648.5}, 57: {"0057": 648.8}, 58: {"0058": 648.3}, 59: {"0059": 649.0}, 60: {"0060": 640.5}, 
    61: {"0061": 639.0}, 62: {"0062": 644.5}, 63: {"0063": 644.5}, 64: {"0064": 645.5}, 65: {"0065": 645.5}, 66: {"0066": 645.5}, 67: {"0067": 645.5}, 68: {"0068": 645.5}, 69: {"0069": 645.5}, 70: {"0070": 645.5}, 
    71: {"0071": 645.5}, 72: {"0072": 645.5}, 73: {"0073": 645.5}, 74: {"0074": 645.5}, 75: {"0075": 645.5}, 76: {"0076": 645.5}, 77: {"0077": 645.5}, 78: {"0078": 645.5}, 79: {"0079": 645.5}, 80: {"0080": 645.5}, 
    81: {"0081": 645.5}, 82: {"0082": 645.5}, 83: {"0083": 645.5}, 84: {"0084": 645.5}, 85: {"0085": 645.5}, 86: {"0086": 645.5}, 87: {"0087": 645.5}, 88: {"0088": 645.5}, 89: {"0089": 645.5}, 90: {"0090": 645.5}, 
    91: {"0091": 645.5}, 92: {"0092": 645.5}, 93: {"0093": 645.5}, 94: {"0094": 645.5}, 95: {"0095": 645.5}, 96: {"0096": 645.5}, 97: {"0097": 645.5}, 98: {"0098": 645.5}, 99: {"0099": 646.5}, 100: {"0100": 645.5},   
    101: {"0101": 645.5}, 102: {"0102": 645.5}, 103: {"0103": 645.5}, 104: {"0104": 645.5}, 105: {"0105": 645.5}, 106: {"0106": 645.5}, 107: {"0107": 645.5}, 108: {"0108": 644.5}, 109: {"0109": 645.5}, 110: {"0110": 644.3}, 
    111: {"0111": 645.0}, 112: {"0112": 645.0}, 113: {"0113": 645.0}, 114: {"0114": 645.5}, 115: {"0115": 645.5}, 116: {"0116": 645.5}, 117: {"0117": 645.5}, 118: {"0118": 645.5}, 119: {"0119": 644.7}, 120: {"0120": 645.5},
    121: {"0121": 645.3}, 122: {"0122": 644.5}, 123: {"0123": 644.0}, 124: {"0124": 645.0}, 125: {"0125": 644.5}, 126: {"0126": 644.5}, 127: {"0127": 642.5}, 128: {"0128": 644.5}, 129: {"0129": 644.0}, 130: {"0130": 645.5}, 
    131: {"0131": 645.5}, 132: {"0132": 645.5}, 133: {"0133": 645.5}, 134: {"0134": 645.5}, 135: {"0135": 645.5}, 136: {"0136": 645.5}, 137: {"0137": 645.8}, 138: {"0138": 646.5}, 139: {"0139": 646.5}, 140: {"0140": 646.5}, 
    141: {"0141": 646.5}, 142: {"0142": 646.7}, 143: {"0143": 647.5}, 144: {"0144": 646.9}, 145: {"0145": 646.8}, 146: {"0146": 646.9}, 147: {"0147": 646.5}, 148: {"0148": 646.5}, 149: {"0149": 646.9}, 150: {"0150": 647.5}, 
    151: {"0151": 647.0}, 152: {"0152": 646.9}, 153: {"0153": 647.5}, 154: {"0154": 648.5}, 155: {"0155": 648.5}, 156: {"0156": 648.5}, 157: {"0157": 648.5}, 158: {"0158": 648.5}, 159: {"0159": 648.5}, 160: {"0160": 648.5}, 
    161: {"0161": 648.5}, 162: {"0162": 648.5}, 163: {"0163": 648.5}, 164: {"0164": 648.5}, 165: {"0165": 648.5}, 166: {"0166": 648.5}, 167: {"0167": 648.5}, 168: {"0168": 648.5}, 169: {"0169": 648.5}, 170: {"0170": 648.5}, 
    171: {"0171": 648.5}, 172: {"0172": 647.5}, 173: {"0173": 646.5}, 174: {"0174": 662.5}, 175: {"0175": 655.5}, 176: {"0176": 648.5}, 177: {"0177": 648.5}, 178: {"0178": 648.5}, 179: {"0179": 648.5}, 180: {"0180": 648.5}, 
    181: {"0181": 648.5}, 182: {"0182": 648.5}, 183: {"0183": 648.5}, 184: {"0184": 648.5}, 185: {"0185": 648.5}, 186: {"0186": 648.5}, 187: {"0187": 648.5}, 188: {"0188": 648.5}, 189: {"0189": 648.5}, 190: {"0190": 648.5}, 
    191: {"0191": 648.5}, 192: {"0192": 648.5}, 193: {"0193": 648.5}, 194: {"0194": 648.5}, 195: {"0195": 648.5}, 196: {"0196": 648.5}, 197: {"0197": 648.5}, 198: {"0198": 648.5}, 199: {"0199": 648.5}, 200: {"0200": 643.5},
    201: {"0201": 648.5}, 202: {"0202": 648.5}, 203: {"0203": 648.5}, 204: {"0204": 648.5}, 205: {"0205": 648.5}, 206: {"0206": 648.5}, 207: {"0207": 648.5}, 208: {"0208": 648.5}, 209: {"0209": 648.5}, 210: {"0210": 648.5}, 
    211: {"0211": 648.5}, 212: {"0212": 648.5}, 213: {"0213": 648.5}, 214: {"0214": 648.5}, 215: {"0215": 648.5}, 216: {"0216": 648.5}, 217: {"0217": 648.5}, 218: {"0218": 648.5}, 219: {"0219": 648.5}, 220: {"0220": 648.5}, 
    221: {"0221": 648.5}, 222: {"0222": 648.5}, 223: {"0223": 648.5}, 224: {"0224": 648.5}, 225: {"0225": 648.5}, 226: {"0226": 647.5}, 227: {"0227": 648.5}, 228: {"0228": 648.5}, 229: {"0229": 648.5}, 230: {"0230": 648.5}, 
    231: {"0231": 648.5}, 232: {"0232": 648.5}, 233: {"0233": 648.5}, 234: {"0234": 648.5}, 235: {"0235": 648.5}, 236: {"0236": 648.5}, 237: {"0237": 648.5}, 238: {"0238": 648.5}, 239: {"0239": 648.5}, 240: {"0240": 648.5}, 
    241: {"0241": 648.5}, 242: {"0242": 648.5}, 243: {"0243": 648.5}, 244: {"0244": 648.5}, 245: {"0245": 648.5}, 246: {"0246": 648.5}, 247: {"0247": 648.5}, 248: {"0248": 648.5}, 249: {"0249": 648.5}, 250: {"0250": 648.5}, 
    251: {"0251": 648.5}, 252: {"0252": 648.5}, 253: {"0253": 648.5}, 254: {"0254": 648.5}, 255: {"0255": 648.5}, 256: {"0256": 648.5}, 257: {"0257": 648.5}, 258: {"0258": 648.5}, 259: {"0259": 648.5}, 260: {"0260": 648.5}, 
    261: {"0261": 648.5}, 262: {"0262": 648.5}, 263: {"0263": 648.5}, 264: {"0264": 648.5}, 265: {"0265": 648.5}, 266: {"0266": 648.5}, 267: {"0267": 648.5}, 268: {"0268": 648.5}, 269: {"0269": 648.5}, 270: {"0270": 648.5}, 
    271: {"0271": 648.5}, 272: {"0272": 648.5}, 273: {"0273": 648.5}, 274: {"0274": 648.5}, 275: {"0275": 648.5}, 276: {"0276": 648.5}, 277: {"0277": 648.5}, 278: {"0278": 648.5}, 279: {"0279": 648.5}, 280: {"0280": 648.5}, 
    281: {"0281": 648.5}, 282: {"0282": 648.5}, 283: {"0283": 648.5}, 284: {"0284": 648.5}, 285: {"0285": 648.5}, 286: {"0286": 648.5}, 287: {"0287": 648.5}, 288: {"0288": 648.5}, 289: {"0289": 648.5}, 290: {"0290": 648.5}, 
    291: {"0291": 648.5}, 292: {"0292": 648.5}, 293: {"0293": 648.5}, 294: {"0294": 648.5}, 295: {"0295": 648.5}, 296: {"0296": 648.5}, 297: {"0297": 648.5}, 298: {"0298": 648.5}, 299: {"0299": 648.5}, 300: {"0300": 648.5},
    301: {"0301": 648.5}, 302: {"0302": 648.5}, 303: {"0303": 648.5}, 304: {"0304": 648.5}, 305: {"0305": 648.5}, 306: {"0306": 648.5}, 307: {"0307": 648.5}, 308: {"0308": 648.5}, 309: {"0309": 648.5}, 310: {"0310": 648.5}, 
    311: {"0311": 648.5}, 312: {"0312": 648.5}, 313: {"0313": 648.5}, 314: {"0314": 648.5}, 315: {"0315": 648.5}, 316: {"0316": 648.5}, 317: {"0317": 648.5}, 318: {"0318": 648.5}, 319: {"0319": 648.5}, 320: {"0320": 648.5}, 
    321: {"0321": 648.5}, 322: {"0322": 648.5}, 323: {"0323": 648.5}, 324: {"0324": 648.5}, 325: {"0325": 648.5}, 327: {"0327": 648.5}, 328: {"0328": 648.5}, 329: {"0329": 648.5}, 
    332: {"0332": 646.2}, 333: {"0333": 646.5}, 334: {"0334": 646.5}, 335: {"0335": 646.5}, 336: {"0336": 647.5}, 337: {"0337": 647.5}, 338: {"0338": 648.5}, 339: {"0339": 648.5}, 340: {"0340": 648.5}, 
    341: {"0341": 648.5}, 342: {"0342": 648.5}, 343: {"0343": 648.5}, 344: {"0344": 648.5}, 345: {"0345": 648.5}, 346: {"0346": 648.5}, 347: {"0347": 648.5}, 348: {"0348": 648.5}, 349: {"0349": 648.5}, 350: {"0350": 648.5}, 
    351: {"0351": 648.5}, 352: {"0352": 648.5}, 353: {"0353": 648.5}, 354: {"0354": 648.5}, 355: {"0355": 648.5}, 356: {"0356": 648.5}, 357: {"0357": 648.5}, 358: {"0358": 648.5}, 359: {"0359": 648.5}, 360: {"0360": 648.5}, 
    361: {"0361": 648.5}, 362: {"0362": 648.5}, 363: {"0363": 648.5}, 364: {"0364": 648.5}, 365: {"0365": 648.5}, 366: {"0366": 648.5}, 367: {"0367": 648.5}, 368: {"0368": 648.5}, 369: {"0369": 648.5}, 370: {"0370": 648.5}, 
    371: {"0371": 648.5}, 372: {"0372": 648.5}, 373: {"0373": 648.5}, 374: {"0374": 648.5}, 375: {"0375": 648.5}, 376: {"0376": 648.5}, 377: {"0377": 648.5}, 378: {"0378": 648.5}, 379: {"0379": 648.5}, 380: {"0380": 648.5}, 
    381: {"0381": 648.5}, 382: {"0382": 648.5}, 383: {"0383": 648.5}, 384: {"0384": 648.5}, 385: {"0385": 648.5}, 386: {"0386": 648.5}, 387: {"0387": 648.5}, 388: {"0388": 648.5}, 389: {"0389": 648.5}, 390: {"0390": 648.5}, 
    391: {"0391": 648.5}, 392: {"0392": 648.5}, 393: {"0393": 648.5}, 394: {"0394": 648.5}, 395: {"0395": 648.5}, 396: {"0396": 648.5}, 397: {"0397": 648.5}, 398: {"0398": 648.5}, 399: {"0399": 648.5}, 400: {"0400": 648.5},
    401: {"0401": 648.5}, 402: {"0402": 648.5}, 404: {"0404": 645.5}, 405: {"0405": 645.5}, 406: {"0406": 648.5}, 407: {"0407": 648.5}, 408: {"0408": 648.5}, 409: {"0409": 648.5}, 410: {"0410": 648.5}, 
    411: {"0411": 648.5}, 412: {"0412": 648.5}, 413: {"0413": 648.5}, 414: {"0414": 648.5}, 415: {"0415": 648.5}, 416: {"0416": 648.5}, 417: {"0417": 648.5}, 418: {"0418": 648.5}, 419: {"0419": 648.5}, 420: {"0420": 648.5}, 
    421: {"0421": 648.5}, 422: {"0422": 648.5}, 423: {"0423": 648.5}, 424: {"0424": 648.5}, 425: {"0425": 648.5}, 426: {"0426": 648.5}, 427: {"0427": 648.5}, 479: {"0479": 649.0}, 480: {"0480": 649.0}, 
    481: {"0481": 649.0}, 482: {"0482": 649.0}, 483: {"0483": 649.0}, 484: {"0484": 649.0}, 485: {"0485": 649.0}, 486: {"0486": 649.0}, 487: {"0487": 649.0}, 488: {"0488": 649.0}, 489: {"0489": 649.0}, 490: {"0490": 649.0}, 
    491: {"0491": 649.0}, 492: {"0492": 649.0}, 493: {"0493": 649.0}, 494: {"0494": 649.0}, 495: {"0495": 649.0}, 496: {"0496": 649.0}, 497: {"0497": 649.0}, 498: {"0498": 649.0}, 499: {"0499": 649.0}, 500: {"0500": 649.0},
    501: {"0501": 649.0}, 502: {"0502": 649.0}, 503: {"0503": 649.0}, 504: {"0504": 649.0}, 505: {"0505": 649.0}, 506: {"0506": 649.0}, 507: {"0507": 649.0}, 508: {"0508": 649.0}, 509: {"0509": 649.0}, 510: {"0510": 649.0}, 
    511: {"0511": 649.0}, 512: {"0512": 649.3}, 513: {"0513": 649.3}, 514: {"0514": 649.3}, 515: {"0515": 649.3}, 516: {"0516": 649.3}, 517: {"0517": 649.3}, 518: {"0518": 649.2}, 519: {"0519": 649.3}, 520: {"0520": 649.0},  
    521: {"0521": 648.8}, 522: {"0522": 648.8}, 523: {"0523": 648.8}, 524: {"0524": 648.8}, 525: {"0525": 648.8}, 526: {"0526": 648.8}, 527: {"0527": 648.8}, 528: {"0528": 648.8}, 529: {"0529": 648.8}, 530: {"0530": 648.8}, 
    531: {"0531": 648.8}, 532: {"0532": 648.8}, 533: {"0533": 648.8}, 534: {"0534": 648.8}, 535: {"0535": 648.8}, 536: {"0536": 648.8}, 537: {"0537": 648.8}, 538: {"0538": 648.8}, 539: {"0539": 648.8}, 540: {"0540": 648.5}, 
    541: {"0541": 648.5}, 542: {"0542": 648.5}, 543: {"0543": 648.5}, 544: {"0544": 648.5}, 545: {"0545": 648.5}, 546: {"0546": 648.5}, 547: {"0547": 648.5}, 548: {"0548": 648.5}, 549: {"0549": 648.5}, 550: {"0550": 648.5}, 
    551: {"0551": 648.5}, 552: {"0552": 648.5}, 553: {"0553": 648.5}, 554: {"0554": 648.5}, 555: {"0555": 648.5}, 556: {"0556": 648.5}, 557: {"0557": 648.5}, 558: {"0558": 648.5}, 559: {"0559": 648.5}, 560: {"0560": 648.5}, 
    561: {"0561": 648.5}, 562: {"0562": 648.5}, 563: {"0563": 648.5}, 564: {"0564": 648.5}, 565: {"0565": 648.5}, 566: {"0566": 648.5}, 567: {"0567": 648.5}, 568: {"0568": 648.5}, 569: {"0569": 648.5}, 570: {"0570": 648.5}, 
    571: {"0571": 648.5}, 572: {"0572": 648.5}, 573: {"0573": 648.5}, 574: {"0574": 648.5}, 575: {"0575": 648.5}, 576: {"0576": 648.5}, 577: {"0577": 648.5}, 578: {"0578": 648.5}, 579: {"0579": 648.5}, 580: {"0580": 648.5}, 
    581: {"0581": 648.5}, 582: {"0582": 648.5}, 583: {"0583": 648.5}, 584: {"0584": 648.5}, 585: {"0585": 648.5}, 586: {"0586": 648.5}, 587: {"0587": 648.5}, 588: {"0588": 648.5}, 589: {"0589": 648.5}, 590: {"0590": 648.5}, 
    591: {"0591": 648.5}, 592: {"0592": 648.5}, 593: {"0593": 648.5}, 594: {"0594": 648.5}, 595: {"0595": 648.5}, 596: {"0596": 648.5}, 597: {"0597": 643.5}, 598: {"0598": 644.5}, 599: {"0599": 644.5}, 600: {"0600": 644.5}, 
    601: {"0601": 644.5}} 
    for key in dictionary:
        dict2 = dictionary[key]
        for key2 in dict2:
            prefix = 'exp_'
            index = key2
            fname = top + prefix + index + '/proj_' + index + '.hdf'
            rot_center = dict2[key2]
            print(fname, rot_center)

