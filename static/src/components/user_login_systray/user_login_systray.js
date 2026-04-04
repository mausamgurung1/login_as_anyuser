/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { cookie } from "@web/core/browser/cookie";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

class UserLoginSystray extends Component {
  static template = "login_as_anyuser.UserLoginSystray";
  static components = { Dropdown, DropdownItem };

  setup() {
    this.ui = useService("ui");
    this.notification = useService("notification");

    this.users = session.switchable_users || [];
    this.isSwitched = session.is_switched || false;
    this.originalUserName = session.original_user_name || "";

    this.state = useState({ busy: false });
  }

  get isSmall() {
    return this.ui.isSmall;
  }

  async _post(route, params = {}) {
    const res = await fetch(route, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Csrf-Token": cookie.get("csrf_token"),
      },
      body: JSON.stringify({ jsonrpc: "2.0", method: "call", id: 1, params }),
    });
    const json = await res.json();
    if (json.error)
      throw new Error(json.error.data?.message || json.error.message);
    return json.result;
  }

  async onUserClick(user) {
    if (this.state.busy) return;
    this.state.busy = true;
    try {
      const result = await this._post("/web/login_as_user", {
        user_id: user.id,
      });
      if (result?.success) {
        window.location.href = "/odoo";
      } else {
        this.notification.add(result?.error || "Could not switch user.", {
          type: "danger",
        });
        this.state.busy = false;
      }
    } catch (e) {
      this.notification.add(e.message || "Network error.", { type: "danger" });
      this.state.busy = false;
    }
  }

  async onSwitchBack() {
    if (this.state.busy) return;
    this.state.busy = true;
    try {
      const result = await this._post("/web/switch_back");
      if (result?.success) {
        window.location.href = "/odoo";
      } else {
        this.notification.add(result?.error || "Could not switch back.", {
          type: "danger",
        });
        this.state.busy = false;
      }
    } catch (e) {
      this.notification.add(e.message || "Network error.", { type: "danger" });
      this.state.busy = false;
    }
  }
}

if (session.can_switch_user) {
  registry
    .category("systray")
    .add(
      "login_as_anyuser.UserLoginSystray",
      { Component: UserLoginSystray },
      { sequence: 1 },
    );
}
