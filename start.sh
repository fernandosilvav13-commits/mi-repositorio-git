#!/usr/bin/env bash
set -e

echo "🚀 Iniciando backend (FastAPI)..."
cd backend
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

echo "🚀 Iniciando frontend (Next.js)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo ""
echo "  Presiona Ctrl+C para detener ambos."
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
