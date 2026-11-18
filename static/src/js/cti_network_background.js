import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";

export class CtiNetworkBackground extends Interaction {
    static selector = ".o_cti_catalog_page";

    setup() {
        this.canvas = this.el.querySelector(".o_cti_network_canvas");
        this.context = this.canvas?.getContext("2d", { alpha: true });
        this.points = [];
        this.frameId = 0;
        this.previousFrame = 0;
        this.pageVisible = !document.hidden;
        this.motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
        this.reduceMotion = this.motionPreference.matches;
        this.drawFrame = this.drawFrame.bind(this);
        this.onResize = this.onResize.bind(this);
        this.onPageResize = this.onPageResize.bind(this);
        this.onVisibilityChange = this.onVisibilityChange.bind(this);
        this.onMotionPreferenceChange = this.onMotionPreferenceChange.bind(this);
    }

    start() {
        if (!this.context) {
            return;
        }
        this.backgroundHost = this.el.closest("#wrapwrap > main") || this.el.parentElement;
        this.backgroundHost.classList.add("o_cti_network_background_host");
        this.backgroundHost.appendChild(this.canvas);
        window.addEventListener("resize", this.onResize, { passive: true });
        window.addEventListener("load", this.onPageResize, { passive: true });
        this.pageResizeObserver = new ResizeObserver(this.onPageResize);
        this.pageResizeObserver.observe(this.backgroundHost);
        document.addEventListener("visibilitychange", this.onVisibilityChange);
        this.motionPreference.addEventListener("change", this.onMotionPreferenceChange);
        this.registerCleanup(() => {
            window.removeEventListener("resize", this.onResize);
            window.removeEventListener("load", this.onPageResize);
            this.pageResizeObserver.disconnect();
            this.canvas.remove();
            this.backgroundHost.classList.remove("o_cti_network_background_host");
            document.removeEventListener("visibilitychange", this.onVisibilityChange);
            this.motionPreference.removeEventListener("change", this.onMotionPreferenceChange);
            cancelAnimationFrame(this.frameId);
        });
        this.resize();
        this.resume();
    }

    resize() {
        this.width = Math.max(1, this.backgroundHost.clientWidth);
        this.height = Math.max(1, this.backgroundHost.scrollHeight);
        this.canvas.style.height = `${this.height}px`;
        this.pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
        this.canvas.width = Math.round(this.width * this.pixelRatio);
        this.canvas.height = Math.round(this.height * this.pixelRatio);
        this.context.setTransform(this.pixelRatio, 0, 0, this.pixelRatio, 0, 0);

        const density = this.width < 600 ? 21000 : 14500;
        const pointCount = Math.max(28, Math.min(115, Math.round((this.width * this.height) / density)));
        this.points = Array.from({ length: pointCount }, () => this.createPoint());
        if (this.reduceMotion) {
            this.renderNetwork(0, false);
        }
    }

    createPoint() {
        const angle = Math.random() * Math.PI * 2;
        const speed = .08 + Math.random() * .16;
        return {
            x: Math.random() * this.width,
            y: Math.random() * this.height,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            radius: 1 + Math.random() * 1.25,
            phase: Math.random() * Math.PI * 2,
            accent: Math.random() > .82,
        };
    }

    onResize() {
        this.resize();
    }

    onPageResize() {
        if (this.width !== Math.max(1, this.backgroundHost.clientWidth) || this.height !== Math.max(1, this.backgroundHost.scrollHeight)) {
            this.resize();
        }
    }

    onVisibilityChange() {
        this.pageVisible = !document.hidden;
        this.resume();
    }

    onMotionPreferenceChange(event) {
        this.reduceMotion = event.matches;
        this.resume();
    }

    resume() {
        cancelAnimationFrame(this.frameId);
        this.frameId = 0;
        this.previousFrame = 0;
        if (!this.pageVisible || !this.context) {
            return;
        }
        if (this.reduceMotion) {
            this.renderNetwork(0, false);
        } else {
            this.frameId = requestAnimationFrame(this.drawFrame);
        }
    }

    drawFrame(timestamp) {
        if (!this.pageVisible) {
            this.frameId = 0;
            return;
        }
        const elapsed = this.previousFrame ? Math.min((timestamp - this.previousFrame) / 16.67, 2) : 1;
        this.previousFrame = timestamp;
        this.renderNetwork(elapsed, true, timestamp);
        this.frameId = requestAnimationFrame(this.drawFrame);
    }

    renderNetwork(elapsed, animate, timestamp = 0) {
        const context = this.context;
        context.clearRect(0, 0, this.width, this.height);
        const linkDistance = this.width < 600 ? 120 : 155;
        const points = this.points;

        if (animate) {
            for (const point of points) {
                point.x += point.vx * elapsed;
                point.y += point.vy * elapsed;
                if (point.x < -5) point.x = this.width + 5;
                if (point.x > this.width + 5) point.x = -5;
                if (point.y < -5) point.y = this.height + 5;
                if (point.y > this.height + 5) point.y = -5;
            }
        }

        context.lineWidth = .8;
        for (let i = 0; i < points.length; i++) {
            const point = points[i];
            for (let j = i + 1; j < points.length; j++) {
                const other = points[j];
                const dx = point.x - other.x;
                const dy = point.y - other.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < linkDistance) {
                    const pulse = animate ? .88 + .12 * Math.sin(timestamp / 1300 + point.phase) : 1;
                    const alpha = (1 - distance / linkDistance) * .36 * pulse;
                    context.strokeStyle = `rgba(48, 112, 144, ${alpha})`;
                    context.beginPath();
                    context.moveTo(point.x, point.y);
                    context.lineTo(other.x, other.y);
                    context.stroke();
                }
            }
        }

        for (const point of points) {
            const pulse = animate ? .85 + .15 * Math.sin(timestamp / 900 + point.phase) : 1;
            context.beginPath();
            context.arc(point.x, point.y, point.radius * pulse, 0, Math.PI * 2);
            context.fillStyle = point.accent
                ? "rgba(51, 126, 132, .68)"
                : "rgba(55, 112, 143, .56)";
            context.fill();
        }
    }
}

registry.category("public.interactions").add("cti_core.network_background", CtiNetworkBackground);
