import { BrowserRouter, Routes, Route } from "react-router";
import Index from "./pages/index";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function App() {
	return (
		<QueryClientProvider client={queryClient}>
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Index />} />
				</Routes>
			</BrowserRouter>
		</QueryClientProvider>
	);
}
