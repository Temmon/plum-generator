% rebase('base.tpl', title='Speech habits')
<% categories = sorted(habits.keys())%>
% for c in categories:
    <p>{{c}}: {{habits[c]}}</p>
% end