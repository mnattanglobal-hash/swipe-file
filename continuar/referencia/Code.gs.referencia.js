/**
 * Backend do Swipe File: login da equipe e seleções salvas.
 * Publicar como App da Web: Executar como "Eu", Acesso "Qualquer pessoa".
 * Os dados ficam numa planilha criada automaticamente na primeira chamada.
 */
const USUARIOS = { /* removido: usuários e senhas serão recriados no servidor novo */ };
const SESSAO_DIAS = 60;

function doPost(e) {
  let body = {};
  try { body = JSON.parse(e.postData.contents || '{}'); } catch (err) { return out({ok:false, erro:'json'}); }
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    if (body.acao === 'login') return out(login(body.usuario, body.senha));
    const u = usuarioDoToken(body.token);
    if (!u) return out({ok:false, erro:'sessao'});
    if (body.acao === 'dados') return out(dados(u));
    if (body.acao === 'salvar') return out(salvar(u, body.ids));
    if (body.acao === 'sair') { sair(body.token); return out({ok:true}); }
    return out({ok:false, erro:'acao'});
  } finally { lock.releaseLock(); }
}
function doGet() { return out({ok:true, servico:'swipe-file'}); }

function out(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
function hash(salt, senha) {
  const b = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, salt + senha, Utilities.Charset.UTF_8);
  return b.map(x => ('0' + (x & 255).toString(16)).slice(-2)).join('');
}
function login(usuario, senha) {
  usuario = String(usuario || '').trim().toLowerCase();
  const reg = USUARIOS[usuario];
  if (!reg || hash(reg.salt, String(senha || '')) !== reg.hash) return {ok:false, erro:'credenciais'};
  const token = Utilities.getUuid() + Utilities.getUuid().slice(0, 8);
  const props = PropertiesService.getScriptProperties();
  props.setProperty('t_' + token, JSON.stringify({u: usuario, exp: Date.now() + SESSAO_DIAS * 864e5}));
  return {ok:true, token: token, usuario: usuario};
}
function usuarioDoToken(token) {
  if (!token) return null;
  const v = PropertiesService.getScriptProperties().getProperty('t_' + token);
  if (!v) return null;
  const s = JSON.parse(v);
  if (s.exp < Date.now()) { PropertiesService.getScriptProperties().deleteProperty('t_' + token); return null; }
  return s.u;
}
function sair(token) { PropertiesService.getScriptProperties().deleteProperty('t_' + token); }

function planilha() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('planilha');
  if (id) { try { return SpreadsheetApp.openById(id).getSheets()[0]; } catch (e) {} }
  const ss = SpreadsheetApp.create('Swipe File - seleções da equipe');
  const sh = ss.getSheets()[0];
  sh.getRange(1, 1, 1, 3).setValues([['usuario', 'ids_selecionados', 'atualizado_em']]);
  props.setProperty('planilha', ss.getId());
  return sh;
}
function lerTudo() {
  const sh = planilha();
  const n = sh.getLastRow();
  const res = {};
  if (n < 2) return res;
  sh.getRange(2, 1, n - 1, 3).getValues().forEach(r => {
    if (r[0]) res[r[0]] = String(r[1] || '').split(',').filter(Boolean);
  });
  return res;
}
function dados(u) {
  const tudo = lerTudo();
  return {ok:true, usuario:u, minhas: tudo[u] || [], equipe: tudo};
}
function salvar(u, ids) {
  if (!Array.isArray(ids)) return {ok:false, erro:'ids'};
  ids = ids.map(String).filter(x => /^\d{5,25}$/.test(x)).slice(0, 2000);
  const sh = planilha();
  const n = sh.getLastRow();
  let linha = -1;
  if (n >= 2) {
    const nomes = sh.getRange(2, 1, n - 1, 1).getValues();
    for (let i = 0; i < nomes.length; i++) if (nomes[i][0] === u) { linha = i + 2; break; }
  }
  if (linha < 0) linha = n + 1;
  sh.getRange(linha, 1, 1, 3).setValues([[u, ids.join(','), new Date()]]);
  return {ok:true, total: ids.length};
}
