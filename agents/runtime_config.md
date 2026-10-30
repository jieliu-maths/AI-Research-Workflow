# Runtime configuration for research roles

Recommended starting configuration. A project owner may approve different
models or reasoning effort for a particular project or task:

| Role | Model | Reasoning effort | Speed |
| --- | --- | --- | --- |
| Research Director | `gpt-5.6-sol` | `high` | standard |
| Researcher | `gpt-5.6-sol` | `xhigh` | standard |
| Critic / Falsifier | `gpt-5.6-sol` | `xhigh` | standard |
| Experimenter | `gpt-5.6-terra` | `high` | standard; fast only for mechanical iterations |

Use `max` only for a sharply defined, stubborn core derivation or final proof
audit. Luna may be used for formatting or bulk mechanical work, not for
adjudicating a central theorem claim. A dispatch-time model/effort override
implements this configuration when a task's saved setting differs.
