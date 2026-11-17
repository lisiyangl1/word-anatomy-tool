// DOM 冒烟测试：用 jsdom 真跑一遍页面脚本，验证渲染 / 折叠 / 复制 / 查无此词
// DOM 冒烟测试：用 jsdom 真跑一遍页面脚本，验证渲染 / 折叠 / 复制 / 查无此词
// 用法：npm i jsdom && node build/domtest.js
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync(path.join(__dirname, '..', 'word-anatomy.html'), 'utf8');

const errors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  url: 'https://localhost/',
  resources: undefined,               // 不加载外部 tailwind，避免网络
  beforeParse(window) {
    // jsdom 缺失的 API 打补丁
    window.HTMLElement.prototype.scrollIntoView = function () {};
    window.speechSynthesis = { cancel() {}, speak() {} };
    window.SpeechSynthesisUtterance = function (t) { this.text = t; };
    window.addEventListener('error', e => errors.push('window error: ' + e.message));
    window.document.addEventListener('DOMContentLoaded', () => {});
  }
});

const { window } = dom;
const { document } = window;
window.addEventListener('unhandledrejection', e => errors.push('rejection: ' + e.reason));

function typeAndSubmit(word) {
  const q = document.querySelector('#q');
  const form = document.querySelector('#searchForm');
  q.value = word;
  q.dispatchEvent(new window.Event('input'));
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  // 等待 renderLoading → 320ms 后 render
  return new Promise(r => setTimeout(r, 450));
}

(async () => {
  await new Promise(r => setTimeout(r, 150));
  const assert = (cond, msg) => console.log((cond ? 'PASS ' : 'FAIL ') + msg);

  console.log('--- 初始化 ---');
  assert(!!document.querySelector('#result').innerHTML.trim(), '空状态已渲染');
  console.log('词库规模显示:', document.querySelector('#dictSize').textContent);

  console.log('\n--- 查询 unbelievable ---');
  await typeAndSubmit('unbelievable');
  const res = document.querySelector('#result');
  const text = res.textContent.replace(/\s+/g, ' ');
  assert(/#result/.test('#result') && res.innerHTML.includes('unbelievable'), '词头渲染');
  assert(res.querySelectorAll('.seg').length === 3, '三个词根词缀色块，实际 ' + res.querySelectorAll('.seg').length);
  assert(res.querySelectorAll('.syl').length === 5, '五个音节，实际 ' + res.querySelectorAll('.syl').length);
  assert(res.querySelectorAll('.meaning').length >= 1, '释义卡');
  assert(res.querySelectorAll('.syn').length === 4, '同义词标签，实际 ' + res.querySelectorAll('.syn').length);
  assert(res.querySelectorAll('mark').length >= 1, '例句高亮');
  assert(res.querySelectorAll('[data-collapse]').length === 5, '五个折叠模块，实际 ' + res.querySelectorAll('[data-collapse]').length);

  console.log('\n--- 折叠交互 ---');
  const btn = res.querySelector('[data-collapse="sec-mean"]');
  const panel = document.querySelector('#sec-mean');
  console.log('初始 aria-expanded =', btn.getAttribute('aria-expanded'), ' maxHeight =', panel.style.maxHeight);
  btn.dispatchEvent(new window.Event('click', { bubbles: true }));
  console.log('点击后 aria-expanded =', btn.getAttribute('aria-expanded'));
  assert(btn.getAttribute('aria-expanded') === 'false', '折叠收起');

  console.log('\n--- 点击同义词跳转 ---');
  const syn = res.querySelector('.syn');
  const target = syn.dataset.w;
  syn.dispatchEvent(new window.Event('click', { bubbles: true }));
  await new Promise(r => setTimeout(r, 450));
  assert(document.querySelector('#q').value === target, '输入框已填入 ' + target);
  assert(document.querySelector('#result').innerHTML.includes(target.slice(0, 4)), '已查询 ' + target);

  console.log('\n--- 不可拆分单词 window ---');
  await typeAndSubmit('window');
  const t2 = document.querySelector('#result').textContent;
  assert(t2.includes('无法拆分'), '给出不可拆分提示');
  assert(document.querySelectorAll('#result .meaning').length >= 1, '释义仍正常显示');
  assert(document.querySelectorAll('#result .syn').length >= 1, '同义词仍正常显示');

  console.log('\n--- 词形还原 running ---');
  await typeAndSubmit('studied');
  const t3 = document.querySelector('#result').textContent;
  assert(t3.includes('按词形变化匹配到原形'), '提示词形还原');
  assert(document.querySelectorAll('#result .meaning').length >= 1, '原形释义渲染');

  console.log('\n--- 查无此词 ---');
  await typeAndSubmit('zzzqqq');
  const t4 = document.querySelector('#result').textContent;
  assert(t4.includes('暂时没有'), '友好提示');

  console.log('\n--- 复制按钮 ---');
  await typeAndSubmit('computer');
  let copied = null;
  window.navigator.clipboard = { writeText: t => { copied = t; return Promise.resolve(); } };
  window.isSecureContext = true;
  document.querySelector('#copyBtn').dispatchEvent(new window.Event('click', { bubbles: true }));
  await new Promise(r => setTimeout(r, 60));
  assert(!!copied && copied.includes('音节') && copied.includes('【释义与例句】'), '复制内容完整（' + (copied ? copied.length : 0) + ' 字符）');
  if (copied) console.log('\n----- 复制文本样例 -----\n' + copied.split('\n').slice(0, 16).join('\n'));

  console.log('\n--- 随机 / 波纹 ---');
  document.querySelector('#randomBtn').dispatchEvent(new window.Event('click', { bubbles: true }));
  await new Promise(r => setTimeout(r, 450));
  assert(document.querySelectorAll('#result .meaning').length >= 1, '随机查询渲染成功');
  const sb = document.querySelector('#submitBtn');
  sb.dispatchEvent(new window.MouseEvent('click', { bubbles: true, clientX: 10, clientY: 10 }));
  assert(sb.querySelectorAll('.ripple').length === 1, '波纹元素已创建');

  console.log('\n--- 运行期错误 ---');
  console.log(errors.length ? errors : '无');
  console.log('\n最终 DOM 字节:', document.body.innerHTML.length);
  process.exit(0);
})();
