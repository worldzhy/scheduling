# Operations Research Model

Define $S$ as the set of studios, $T$ as the sets of timeslots, $D$ as the set of days, $P$ as the sets of programs, and $C$ as the set of coaches. Also, define the following:

- $q_{pc}$: the qualification of coach $c$ to teach program $p$ ($1$ if qualified, $0$ otherwise).
- $p_{stdpc}$: the profit when coach $c$ teaches program $p$ at studio $s$ on day $d$ at time $t$.

Let $x_{stdpc}$ be defined such that if $x_{stdpc} = 1$, then coach $c$ is scheduled to teach program $p$ at studio $s$ on day $d$ at time $t$. We formulate as follows.

$$
\begin{alignat*}{3}
\text{maximize  }  & \sum_{s \in S} \sum_{t \in T} \sum_{d \in D} \sum_{p \in P} \sum_{c \in C} p_{stdpc} x_{stdpc} && \\
\text{subject to  }
& \sum_{p \in P} \sum_{c \in C} x_{stdpc} = 1,
&& \qquad \forall S \in S, \forall t \in T , \forall d \in D  \\
& \sum_{s \in S} \sum_{t \in T} \sum_{d \in D} x_{stdpc} = 0
&& \qquad \forall p \in P, \forall c \in C \text{ where } q_{pc} = 0\\
& 0 \le x_{stdpc} \le 1,
&& \qquad \forall s \in S, \forall t \in T, \forall d \in D, \forall p \in P, \forall c \in C
\end{alignat*}
$$
