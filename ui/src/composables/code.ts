import {ref, computed} from 'vue';
// @ts-ignore
import CryptoJS from 'crypto-js';

export function cipher() {
    const key = CryptoJS.enc.Utf8.parse('QWERTYUIOPa00000');
    const iv = CryptoJS.enc.Utf8.parse('0000000000000000')
  
    /**
     * 
     * @param text 要加密的原文
     * @returns 返回加密的密文
     */
    function encrypt(text:string){
        var str = text
        return CryptoJS.AES.encrypt(
          str, key, 
          { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.ZeroPadding}
          ).toString()
    }

    /**
     * 
     * @param text 要解密的密文
     * @returns 返回解密的原文
     */
    function decrypt(text:string){
        let re = CryptoJS.AES.decrypt(
          text, key, 
          { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.ZeroPadding}
          ).toString(CryptoJS.enc.Utf8)
        return re
      }
  
    return {
      key,
      iv,
      encrypt,
      decrypt,
    };
}

