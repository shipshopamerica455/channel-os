# procedural-audio

`music.py` and `dsp.py`, lifted from the aiTrends 2D Studio plugin
(`YOUTUBE CHANNELS/CLAUDE PLUGIN/aitrends-2d-studio.plugin`), which generates a
mood-driven score locally with numpy and scipy — no API, no credits, ~67x realtime.

Vendored rather than referenced because the plugin is a zip in a channel folder, not an
installed dependency, and a bed generator that silently stops working when that file
moves is worse than a copy. Only these two files are needed; the rest of the plugin is
a stick-figure animation engine with no bearing on this channel.

Used by `gen-bed.mjs --bed p` for the FOCUS lane only. Deliberately not for sleep: the
harmony is a four-chord progression on a 27-second cycle, which is ~270 passes across a
two-hour focus video and ~1,300 across a ten-hour sleep one. The sleep lane is 87% of
the channel's genuine watch hours and is not worth risking on that.

Upstream is unmodified. Re-extract from the plugin to update.
