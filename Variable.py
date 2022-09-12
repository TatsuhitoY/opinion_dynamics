# omega

num_agents = 100
num_links = 400

num_media_agents = 3
num_media_links = 120
#n_media_links/n_media_linksは整数になるべき
sns_seed = 1
l = 10 # screen size
t_max = 10000 # max steps
epsilon = 0.4 # bounded confidence parameter
mu = 0.5 # social influence strength
p = 0.5 # repost rate
q = 0.5 # rewiring rate
extended_model = True
extended_media_model = True
b = 0.1 # rate of selectable agent 拡張版の時にエージェントの選択確率は　b+opinion/合計
c = 0.1 # rate of selectable media agent 拡張版の時にエージェントの選択確率は　b+opinion/合計
# メディアをなくしたければf=0
f = 0.05 # media post rate
delta = 0.1 # bounded confidence parameter for media agents
# omega = 0.2 # influence strength for media
a = "none"
#opinion_listの要素数はnum_media_agentsと一致する
# opinion_list = [-0.6, -0.2, 0.2, 0.6]
opinion_list = [-2/3, 0, 2/3]

method = 2
if method == 1:
  following_methods = ['Random']
elif method == 2:
  following_methods = ['Repost']
elif method == 3:
  following_methods = ['Recommendation']

media_method = 2
if media_method == 1:
  change_methods = "neighbor"
elif media_method == 2:
  change_methods = "opinion_poll"

size = [200]*num_agents + [1000]*num_media_agents

def draw_h(G, pos, measures, size, list_mode, num_agents, num_media_agents):
  if list_mode:
    result = [measures.iloc[-1, i] for i in range(G.number_of_nodes())]
    dict_measure = nx.degree_centrality(G)
    result2 = list(dict_measure.keys())
    vmin_t = -1.0
    vmax_t = 1.0
  else:
    result = measures
    result2 = [i for i in range(num_agents+num_media_agents)]
    # result = list(measures.values())
    # result2 = list(measures.keys())
    vmin_t = 0.0
    vmax_t = 60.0
  nodes = nx.draw_networkx_nodes(G, pos, node_size = size,
                                 cmap = plt.cm.plasma,                   #matplotlibのcolormapを入力
                                 node_color = result,
                                 nodelist = result2)     #posは辞書型、list(measures.values())で辞書のインデックスの方をリストに格納リストに格納
  nodes.set_norm(mcolors.SymLogNorm(linthresh = 0.1, linscale = 1, vmin = vmin_t, vmax = vmax_t))   #?
  # labels = nx.draw_networkx_labels(G, pos)
  edges = nx.draw_networkx_edges(G, pos)                               #エッジを出力
  plt.colorbar(nodes)                                                #カラーバーを出力

##########################################################################################################################################################

i = 0
plt.figure(figsize=(32,22))
for omega in range(0, 101, 25):
  i += 1
  omega = omega / 100
  # now_str = pd.datetime.now().strftime('%Y%m%d%H%M%S')
  # data_root_dir = os.path.join('data_'+''.join(now_str))
  data_root_dir = "none"
  s = datetime.datetime.now()
  d = EchoChamberDynamics(num_agents, num_media_agents, num_links, num_media_links, epsilon, sns_seed, l, data_root_dir, opinion_list)
  df_opinion, df_screen, df_media_opinion, graph = d.evolve(t_max, mu, p, q, following_methods, b, c, f, change_methods, num_agents, num_media_agents, delta, omega)
  # color_list = [e.opinion for e in d.agents] + [g.media_opinion for g in d.medias]
  e = datetime.datetime.now()
  print("  {0}/{1}".format(i, 5), "Computation Time：", e - s)
  if i == 1:
    first = s
  if i == 5:
    print("Total Computation Time", e - first)

  plt.subplot(6, 5, 5*i-4)
  plt.tight_layout()
  plt.xlim(0, t_max)
  plt.ylim(-1, 1)
  plt.title("agents omega = {0}".format(omega))
  plt.plot(df_opinion)

  plt.subplot(6, 5, 5*i-3)
  plt.tight_layout()
  plt.xlim(0, t_max)
  plt.ylim(-1, 1)
  plt.title("media omega = {0}".format(omega))
  plt.plot(df_media_opinion)

  plt.subplot(6, 5, 5*i-2)
  plt.tight_layout()
  plt.title("opinion_graph")
  df_new = pd.concat([df_opinion, df_media_opinion], axis='columns', ignore_index=True)
  pos=nx.nx_pydot.graphviz_layout(graph)
  draw_h(graph, pos, df_new, size, True, num_agents, num_media_agents)

  plt.subplot(6, 5, 5*i-1)
  plt.tight_layout()
  plt.title("in_degree_graph")
  list_new = [i[1] for i in graph.in_degree()]
  pos=nx.nx_pydot.graphviz_layout(graph)
  draw_h(graph, pos, list_new, size, False, num_agents, num_media_agents)
  # draw_h(graph, pos, graph.in_degree_centrality(), size, False, num_agents, num_media_agents)

  plt.subplot(6, 5, 5*i)
  hist_list = [i[1] for i in graph.in_degree()]
  plt.ylim(0,80)
  plt.title("in_degree histogram")
  plt.hist(hist_list, range=(0, 60), bins = [2*i for i in range(0, 31)], color='#0000CD')
dt = datetime.datetime.today()
print(dt)
plt.tight_layout(rect=[0,0,1,0.92])
plt.suptitle("\n num_agents={0}, num_links={1}, num_media_agents={2}, num_media_links={3}, screen_size={4}, t_max={5}, epsilon={6}, mu={7}, p={8}, q={9}, \n extended_model={10}, extended_media_model={11}, b={12}, c={13}, f={14}, delta={15}, omega={16}, agent_method={17}, media_method={18}".
             format(num_agents, num_links, num_media_agents, num_media_links, l, t_max, epsilon, mu, p, q, extended_model, extended_media_model, b, c, f, delta, a, following_methods, change_methods)
,fontsize=22)