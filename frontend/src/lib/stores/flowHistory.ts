// lib/stores/flowHistory.ts
import { writable } from 'svelte/store';

export const createHistoryStore = () => {
  const { subscribe, set, update } = writable({
    past: [],
    present: null,
    future: []
  });

  return {
    subscribe,
    pushState: (state) => update(h => ({
      past: [...h.past, h.present],
      present: state,
      future: []
    })),
    undo: () => update(h => ({
      past: h.past.slice(0, -1),
      present: h.past[h.past.length - 1],
      future: [h.present, ...h.future]
    })),
    redo: () => update(h => ({
      past: [...h.past, h.present],
      present: h.future[0],
      future: h.future.slice(1)
    }))
  };
};