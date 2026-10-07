import { onRequestPatch as __api_rfqs__id__js_onRequestPatch } from "/Users/shangdizhishou/Documents/Codex/2026-08-22/referenced-chatgpt-conversation-this-is-an-3/work/vietchiphub-v1/functions/api/rfqs/[id].js"
import { onRequestGet as __api_health_js_onRequestGet } from "/Users/shangdizhishou/Documents/Codex/2026-08-22/referenced-chatgpt-conversation-this-is-an-3/work/vietchiphub-v1/functions/api/health.js"
import { onRequestPost as __api_rfq_js_onRequestPost } from "/Users/shangdizhishou/Documents/Codex/2026-08-22/referenced-chatgpt-conversation-this-is-an-3/work/vietchiphub-v1/functions/api/rfq.js"
import { onRequestGet as __api_rfqs_js_onRequestGet } from "/Users/shangdizhishou/Documents/Codex/2026-08-22/referenced-chatgpt-conversation-this-is-an-3/work/vietchiphub-v1/functions/api/rfqs.js"

export const routes = [
    {
      routePath: "/api/rfqs/:id",
      mountPath: "/api/rfqs",
      method: "PATCH",
      middlewares: [],
      modules: [__api_rfqs__id__js_onRequestPatch],
    },
  {
      routePath: "/api/health",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_health_js_onRequestGet],
    },
  {
      routePath: "/api/rfq",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_rfq_js_onRequestPost],
    },
  {
      routePath: "/api/rfqs",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_rfqs_js_onRequestGet],
    },
  ]