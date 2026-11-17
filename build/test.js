// 逻辑自测：抽取页面内联脚本的「数据层 + 算法层」，在 node 中验证
// 算法自测：抽取页面内联脚本的「数据层 + 算法层」，在 node 中验证
// 用法：node build/test.js   （无需安装依赖）
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'word-anatomy.html'), 'utf8');
const start = html.indexOf('const WORDS = [');
const end = html.indexOf('* 4. 工具函数');
let code = html.slice(start, end);
// 去掉末尾未闭合的注释块
code = code.replace(/\/\*\s*-+\s*$/, '');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(code + '\nthis.API={syllabify,decompose,WORD_MAP,WORD_LIST,suggest,lemmaCandidates,rootAt,rootChain,suffixOf};', ctx);
const { syllabify, decompose, WORD_MAP, WORD_LIST, suggest, lemmaCandidates } = ctx.API;

console.log('词库条数:', WORD_LIST.length);

const words = ['unbelievable','international','computer','abandon','beautiful','education','television',
  'window','happy','environment','government','attractive','extraordinary','impossible','unhappy',
  'dictionary','concentrate','underestimate','multicolor','transformation','apple','study',
  'communication','responsibility','unfortunately','biotechnology','subconscious','irreplaceable'];

for (const w of words) {
  const d = decompose(w);
  const segs = d.segs.map(s => `${s.t}(${s.k}:${s.m})`).join(' + ');
  console.log(`${w.padEnd(18)} | ${d.syl.join('·').padEnd(22)} | ${d.unsplittable ? '【不可拆分】' : segs}`);
}

console.log('\n--- 词形还原 ---');
console.log('running ->', lemmaCandidates('running').filter(w => WORD_MAP.has(w)));
console.log('studies ->', lemmaCandidates('studies').filter(w => WORD_MAP.has(w)));
console.log('happier ->', lemmaCandidates('happier').filter(w => WORD_MAP.has(w)));

console.log('\n--- 纠错 ---');
console.log(suggest('beleive'));
console.log(suggest('computor'));

console.log('\n--- 数据抽样 ---');
const e = WORD_MAP.get('abandon');
console.log(JSON.stringify(e, null, 0).slice(0, 400));
