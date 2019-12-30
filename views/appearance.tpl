% rebase('base.tpl', title='Character')
<p>A {{appearance.height}} {{appearance.noun}} with {{appearance.eyeColor}} eyes, {{appearance.hair}}{{appearance.length}} hair, and {{appearance.skinColor}} skin.</p>
<p>Positive Traits: {{positive}}</p>
<p>Negative Traits: {{negative}}</p>
<p>Need: {{need}}</p>
<p>Childhood events: {{events}}</p>
<p>Big five: {{bigfive}}</p>
<p>MBTI: {{mbti}}</p>
<br />
<% categories = sorted(speech.keys())%>
% for c in categories:
    <p>{{c}}: {{speech[c]}}</p>
% end